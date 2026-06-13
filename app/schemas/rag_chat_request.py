from pydantic import BaseModel


class RagChatRequest(BaseModel):
    message: str
