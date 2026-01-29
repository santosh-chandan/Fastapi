import strawberry
import asyncio
from typing import AsyncGenerator

@strawberry.type
class UserSubscription:
    @strawberry.subscription
    async def user_counter(self, info, limit: int = 5) -> AsyncGenerator[int, None]:
        for i in range(limit):
            await asyncio.sleep(1)          # This is exactly like an async generator
            yield i                         # Strawberry maps yield → WebSocket push


# Client GraphQL:

# subscription {
#   userCounter(limit: 3)
# }
