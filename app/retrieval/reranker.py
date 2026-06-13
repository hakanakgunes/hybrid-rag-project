import numpy as np


class Reranker:
    def __init__(self, embedder, vector_store) -> None:
        self.embedder = embedder
        self.vector_store = vector_store

    def rerank(
        self,
        question: str,
        results: list[tuple[str, float]],
    ) -> list[tuple[str, float]]:
        rerank_input = results[:10]

        chunks_embeddings = self.vector_store.get_embeddings(
            [doc for doc, _ in rerank_input]
        )
        chunks_embeddings = np.array(chunks_embeddings)

        query_emb = self.embedder.embed([question])[0]

        return self.embedder.rerank(
            query_emb, rerank_input, chunks_embeddings, top_k=10
        )
