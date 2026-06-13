import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.data.documents import raw_docs
from app.routers import chat_router, llm_router, rag_router
from app.core.dependencies import get_embedding_service, set_rag_service
from app.retrieval.bm25_service import BM25Service
from app.retrieval.query_processor import QueryProcessor
from app.retrieval.reranker import Reranker
from app.retrieval.vector_store import VectorStore
from app.services.chunk_service import ChunkService
from app.services.hybrid_retriever import HybridRetriever
from app.services.llm_service import generate_text, stream_generate_text
from app.services.rag_service import RAGService

services = {}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    services["chunk_service"] = ChunkService()

    docs = raw_docs.strip()
    all_chunks = services["chunk_service"].chunk_text(docs, chunk_size=80, overlap=20)

    services["bm25_service"] = BM25Service(all_chunks)
    services["embedding_service"] = get_embedding_service()
    embeddings = services["embedding_service"].embed(all_chunks)
    services["vector_store"] = VectorStore(all_chunks, embeddings)

    services["reranker"] = Reranker(
        services["embedding_service"],
        services["vector_store"],
    )
    services["query_processor"] = QueryProcessor(generate_text)
    services["retriever"] = HybridRetriever(
        services["embedding_service"],
        services["vector_store"],
        services["bm25_service"],
    )
    services["rag_service"] = RAGService(
        services["reranker"],
        services["retriever"],
        services["query_processor"],
        stream_generate_text,
    )
    set_rag_service(services["rag_service"])

    yield

    services.clear()

app = FastAPI(lifespan=lifespan)

app.include_router(chat_router.router)
app.include_router(llm_router.router)
app.include_router(rag_router.router)
