SHORT_QUERY_THRESHOLD = 4
MAX_GENERATED_QUERIES = 3


class QueryProcessor:
    def __init__(self, generator) -> None:
        self.generator = generator

    def generate_queries(self, question: str) -> list[str]:
        queries = [question]

        if len(question.split()) <= SHORT_QUERY_THRESHOLD:
            queries.append(f"{question} meaning use purpose")

        else:
            mq = self._multi_query(question)

            for q in mq:
                if self._is_relevant(question, q):
                    queries.append(q)

        return queries[:MAX_GENERATED_QUERIES]

    def _multi_query(self, query: str) -> list[str]:
        prompt = f"""
Generate exactly 3 search queries.

Rules:
- Each query on a new line
- No numbering
- No explanations
- No quotes

Query: {query}
"""
        result = self.generator(prompt)
        queries = []

        for line in result.split("\n"):
            q = line.strip()
            if not q:
                continue

            q = q.lstrip("1234567890. ").strip('"').strip()
            queries.append(q)

        return queries[:MAX_GENERATED_QUERIES]

    def _is_relevant(self, original: str, q: str) -> bool:
        original_words = set(original.lower().split())
        q_words = set(q.lower().split())

        overlap = len(original_words & q_words)

        return overlap >= 1
