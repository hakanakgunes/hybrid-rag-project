from app.eval.eval_data import eval_data


def precision_at_k(retrieved, relevant, k=3):
    retrieved_k = [doc for doc, _ in retrieved[:k]]
    hits = sum([1 for doc in retrieved_k if doc in relevant])
    return hits / len(retrieved_k)


def recall_at_k(retrieved, relevant, k=3):
    if not relevant:
        return 1.0

    retrieved_k = [doc for doc, _ in retrieved[:k]]
    hits = sum([1 for doc in relevant if doc in retrieved_k])
    return hits / len(relevant)


def mrr(retrieved, relevant):
    for i, (doc, _) in enumerate(retrieved):
        if doc in relevant:
            return 1 / (i + 1)
    return 0

async def run_eval(rag_service):
    p_scores = []
    r_scores = []
    mrr_scores = []

    for item in eval_data:
        question = item["question"]
        relevant = item["relevant_docs"]

        retrieved = rag_service.retrieve_only(question)

        p = precision_at_k(retrieved, relevant, k=3)
        r = recall_at_k(retrieved, relevant, k=3)
        m = mrr(retrieved, relevant)

        p_scores.append(p)
        r_scores.append(r)
        mrr_scores.append(m)

        print("\n---")
        print("Q:", question)
        print("Top 3:", [doc for doc, _ in retrieved[:3]])
        print("Precision@3:", p)
        print("Recall@3:", r)
        print("MRR:", m)

    print("\n==== FINAL ====")
    print("Avg Precision@3:", sum(p_scores) / len(p_scores))
    print("Avg Recall@3:", sum(r_scores) / len(r_scores))
    print("Avg MRR:", sum(mrr_scores) / len(mrr_scores))
