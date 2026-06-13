from app.core.config import Settings, settings
from app.services.embedding_service import EmbeddingService

rag_service_instance = None
embedding_service_instance = EmbeddingService()

def get_settings() -> Settings:
    return settings

def set_rag_service(service):
    global rag_service_instance
    rag_service_instance = service

def get_rag_service():
    return rag_service_instance

def get_embedding_service():
    return embedding_service_instance