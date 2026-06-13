from pydantic import BaseModel

class ChatResponse(BaseModel):
    answer: str
    request_id: str