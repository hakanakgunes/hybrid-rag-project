from rank_bm25 import BM25Okapi


class BM25Service:
    def __init__(self, documents: list[str]) -> None:
        self.tokenized_docs = [doc.lower().split() for doc in documents]
        self.bm25 = BM25Okapi(self.tokenized_docs)
        self.documents = documents

    def search(self, query: str, top_k: int = 3) -> list[tuple[str, float]]:
        tokenized_query = query.lower().split()
        scores = self.bm25.get_scores(tokenized_query)
        ranked = sorted(zip(self.documents, scores), key=lambda x: x[1], reverse=True)
        return ranked[:top_k]
