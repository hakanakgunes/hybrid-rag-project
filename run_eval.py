import asyncio

from app.data.documents import raw_docs
from app.eval.eval_runner import run_eval
from app.retrieval.bm25_service import BM25Service
from app.retrieval.query_processor import QueryProcessor
from app.retrieval.reranker import Reranker
from app.retrieval.vector_store import VectorStore
from app.services.chunk_service import ChunkService
from app.services.embedding_service import EmbeddingService
from app.services.hybrid_retriever import HybridRetriever
from app.services.llm_service import generate_text, stream_generate_text
from app.services.rag_service import RAGService


# Mirrors the application startup wiring for local retrieval evaluation.
chunk_service = ChunkService()
docs = raw_docs.strip()

all_chunks = chunk_service.smart_chunk(docs, chunk_size=100)

embedding_service = EmbeddingService()
embeddings = embedding_service.embed(all_chunks)

vector_store = VectorStore(all_chunks, embeddings)
bm25_service = BM25Service(all_chunks)

reranker = Reranker(embedding_service, vector_store)
query_processor = QueryProcessor(generate_text)
retriever = HybridRetriever(embedding_service, vector_store, bm25_service)
rag_service = RAGService(reranker, retriever, query_processor, stream_generate_text)

asyncio.run(run_eval(rag_service))
