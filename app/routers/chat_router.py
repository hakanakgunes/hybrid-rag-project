import logging
from uuid import uuid4

from fastapi import APIRouter, Depends

from app.core.config import Settings
from app.core.dependencies import get_settings
from app.schemas.chat_request import ChatRequest
from app.schemas.chat_response import ChatResponse
from app.services.chat_service import generate_answer

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("")
async def get_chat(req: ChatRequest, settings: Settings = Depends(get_settings)):
    logger.info("Handling chat request for app: %s", settings.app_name)
    answer = await generate_answer(req.prompt)
    return ChatResponse(answer=answer, request_id=uuid4())
