
import asyncio

# Websocket: Live Chat asyncGenerator
async def live_chat(message: str):
    yield "Hello"

    for i in range(5):
        await asyncio.sleep(1)
        yield f" chunk {i+1}  for: {message}"

    yield "Ok byee"
