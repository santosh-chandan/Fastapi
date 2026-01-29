from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ChatMessageIn(BaseModel):
    user_id: int
    conversation_id: str
    role: str
    content: str
    embedding: Optional[List[float]] = None  # for RAG

# Outgoing chat message
class ChatMessageOut(BaseModel):
    id: str
    created_at: datetime

# Chat Question
class ChatRequest(BaseModel):
    question: str
