class HybridRetriever:
    def __init__(self, embedder, vector_store, bm25_service) -> None:
        self.embedder = embedder
        self.vector_store = vector_store
        self.bm25 = bm25_service

    def retrieve(
        self,
        queries: list[str],
    ) -> tuple[list[tuple[str, float]], list[tuple[str, float]]]:
        all_dense = []
        all_sparse = []

        for q in queries:
            q_emb = self.embedder.embed(q)
            dense = self.vector_store.faiss_search(q_emb)
            sparse = self.bm25.search(q)

            all_dense.extend(dense)
            all_sparse.extend(sparse)

        return all_dense, all_sparse
