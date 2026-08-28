from pydantic import BaseModel
from typing import Optional


class ChatMessagePayload(BaseModel):
    message: str
    conversation_id: Optional[str] = None
