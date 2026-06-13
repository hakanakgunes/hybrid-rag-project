from collections import defaultdict
from collections.abc import AsyncGenerator, Callable, Iterable
import logging
import time

logger = logging.getLogger(__name__)

MAX_CONTEXT_CHARS = 500
RERANK_THRESHOLD = 0.4
TOP_K_RESULTS = 3
HYBRID_ALPHA = 0.7


class RAGService:
    def __init__(
        self,
        reranker,
        hybrid_retriever,
        query_processor,
        generator: Callable[[str], Iterable[str]],
    ) -> None:
        self.reranker = reranker
        self.retriever = hybrid_retriever
        self.query_processor = query_processor
        self.generator = generator
        self.query_cache = {}

    def _rrf(self, rank: int, k: int = 60) -> float:
        return 1 / (k + rank)

    def _merge_results(
        self,
        dense_results: list[tuple[str, float]],
        sparse_results: list[tuple[str, float]],
        alpha: float = HYBRID_ALPHA,
    ) -> list[tuple[str, float]]:
        scores = defaultdict(float)

        for rank, (doc, score) in enumerate(dense_results):
            if score < RERANK_THRESHOLD:
                continue
            scores[doc] += alpha * self._rrf(rank)

        for rank, (doc, score) in enumerate(sparse_results):
            if score <= 0:
                continue
            scores[doc] += (1 - alpha) * self._rrf(rank)

        return sorted(scores.items(), key=lambda x: x[1], reverse=True)

    def retrieve_only(self, question: str) -> list[tuple[str, float]]:
        queries = self.query_processor.generate_queries(question)
        logger.info("Final retrieval queries: %s", queries)
  
        dense, sparse = self.retriever.retrieve(queries)
        hybrid_results = self._merge_results(dense, sparse, alpha=HYBRID_ALPHA)

        seen = set()
        unique_results = []
        for doc, score in hybrid_results:
            if doc not in seen:
                seen.add(doc)
                unique_results.append((doc, score))

        reranked_results = self.reranker.rerank(question, unique_results)

        filtered_results = [
            (doc, score) for doc, score in reranked_results if score > RERANK_THRESHOLD
        ]

        return filtered_results[:TOP_K_RESULTS]
        
    async def ask(self, question: str) -> AsyncGenerator[str, None]:
        logger.info("Question: %s", question)
        start = time.time()
        
        top_docs = self.retrieve_only(question)
       
        if not top_docs:
            yield "No relevant context found"
            return

        context = ""

        for i, (doc, _) in enumerate(top_docs):
            if len(context) + len(doc) > MAX_CONTEXT_CHARS:
                break
            context += f"[{i+1}] {doc}\n"

        prompt = f"""
You are a strict AI assistant.

You are given multiple context items.

You MUST use ALL relevant items.

If multiple items contain useful information, combine them.

Do NOT ignore any relevant context.

If the answer is not in the context, respond ONLY with:
"I don't know"

Do not provide any additional explanation.

Context:
{context}

Question:
{question}

Answer:
"""
        full_response = ""
        try:
            for token in self.generator(prompt):
                full_response += token
                yield token
        except Exception as e:
            logger.error("Streaming error: %s", e)
            yield "Something went wrong"

        end = time.time()
        logger.info("Response time: %.2f seconds", end - start)
