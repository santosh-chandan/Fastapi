from fastapi.responses import StreamingResponse
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.chat.service import stream_chat, save_message
from app.chat.schemas import ChatMessageIn, ChatRequest
from app.core.engine_psgl import get_db

chat_router = APIRouter()


# -------------------
# SSE (LLM streaming)
# -------------------
@chat_router.get('/chat')
async def do_chat(
    data: ChatRequest, 
    db: AsyncSession = Depends(get_db)
):
    return StreamingResponse(
        stream_chat(data.question, db),
        media_type="text/event-stream"
    )

# -------------------
# Save Chat Message
# -------------------
@chat_router.post('/message')
async def save_chat_message(data: ChatMessageIn):
    return await save_message(data.model_dump())
