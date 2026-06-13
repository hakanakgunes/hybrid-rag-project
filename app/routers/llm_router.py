from fastapi import APIRouter

from app.schemas.generate_request import GenerateRequest
from app.schemas.generate_response import GenerateResponse
from app.services.llm_service import generate_async

router = APIRouter(prefix="/generate", tags=["generate"])


@router.post("")
async def generate(req: GenerateRequest) -> GenerateResponse:
    text = await generate_async(req.prompt)
    return GenerateResponse(text=text)
