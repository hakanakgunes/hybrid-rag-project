class ChunkService:
    def __init__(self, chunk_size: int = 100, overlap: int = 20) -> None:
        self.chunk_size = chunk_size
        self.overlap = overlap

    def split_by_newline(self, text: str) -> list[str]:
        return [line.strip() for line in text.split("\n") if line.strip()]

    def chunk_text(self, text: str, chunk_size: int, overlap: int) -> list[str]:
        words = text.split()
        chunks = []
        self.chunk_size = chunk_size
        self.overlap = overlap

        for i in range(0, len(words), self.chunk_size - self.overlap):
            chunk = words[i : i + self.chunk_size]
            chunks.append(" ".join(chunk))

        return chunks

    def smart_chunk(self, text: str, chunk_size: int = 300) -> list[str]:
        sentences = text.split(".")
        chunks = []
        current = ""

        for sentence in sentences:
            if len(current) + len(sentence) < chunk_size:
                current += sentence + "."
            else:
                chunks.append(current.strip())
                current = sentence + "."

        if current:
            chunks.append(current.strip())

        return chunks
