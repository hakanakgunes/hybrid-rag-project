from sentence_transformers import SentenceTransformer, util


class EmbeddingService:
    def __init__(self) -> None:
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def embed(self, text):
        return self.model.encode(text)

    def rerank(self, query_embedding, results, chunks_embeddings, top_k: int = 2):
        chunks = [doc for doc, _ in results]

        similarities = util.cos_sim(query_embedding, chunks_embeddings)[0]

        ranked_results = list(zip(chunks, similarities))
        sorted_results = sorted(ranked_results, key=lambda x: x[1], reverse=True)

        return sorted_results[:top_k]
