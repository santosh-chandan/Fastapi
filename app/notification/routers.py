from fastapi.responses import StreamingResponse
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.notification.service import live_chat

notification_router = APIRouter()

# -------------------
# WebSocket (Live chat)
# -------------------
@notification_router.websocket('/chat')
async def websocket_chat(websockets: WebSocket):
    await websockets.accept()
    try:
        while True:
            message = await websockets.receive_text()
            async for chunk  in live_chat(message):
                await websockets.send_text(chunk)
    except WebSocketDisconnect:
            print("Client Disconneted")
