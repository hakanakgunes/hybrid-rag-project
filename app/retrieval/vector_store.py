import faiss
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class VectorStore:
    def __init__(self, chunks: list[str], embeddings) -> None:
        self.chunks = chunks
        self.embeddings = np.array(embeddings).astype("float32")
        self.doc_to_embedding = {
            doc: emb / np.linalg.norm(emb) for doc, emb in zip(chunks, embeddings)
        }

        faiss.normalize_L2(self.embeddings)

        dim = self.embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dim)
        self.index.add(self.embeddings)

    def get_embeddings(self, chunks: list[str]) -> list:
        return [self.doc_to_embedding[doc] for doc in chunks]

    def search(self, query_vector, top_k: int = 1) -> list[tuple[str, float]]:
        similarities = cosine_similarity([query_vector], self.embeddings)[0]
        idx = similarities.argsort()[-top_k:][::-1]

        return [(self.chunks[i], similarities[i]) for i in idx]

    def faiss_search(self, query_vector, top_k: int = 3) -> list[tuple[str, float]]:
        query_vector = np.array([query_vector]).astype("float32")

        faiss.normalize_L2(query_vector)

        scores, indices = self.index.search(query_vector, top_k)

        results = []

        for i, score in zip(indices[0], scores[0]):
            results.append((self.chunks[i], float(score)))

        return results
