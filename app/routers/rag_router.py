from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.dependencies import get_rag_service
from app.schemas.rag_chat_request import RagChatRequest

limiter = Limiter(key_func=get_remote_address)
router = APIRouter()


@router.get("/ask")
async def ask(request: str, rag_service=Depends(get_rag_service)):
    return await rag_service.ask(request)


@router.post("/chat/stream")
@limiter.limit("5/minute")  # 5 requests per minute
async def chat_stream(
    request: Request,
    req: RagChatRequest,
    rag_service=Depends(get_rag_service),
):
    async def stream():
        async for token in rag_service.ask(req.message):
            yield token

    return StreamingResponse(stream(), media_type="text/plain")
