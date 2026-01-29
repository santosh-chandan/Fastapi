from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import MONGO_DB_URL, MONGO_DB

# This class acts as a GLOBAL HOLDER for Mongo client
# - Avoids circular imports
# - Allows access from anywhere in the app
# - Ensures SINGLE Mongo connection (singleton pattern)
class MongoDB:
    client: AsyncIOMotorClient | None = None

mongo = MongoDB()

async def connect_mongo():
    mongo.client = AsyncIOMotorClient(MONGO_DB_URL)

async def close_mongo():
    mongo.client.close()

async def get_database():
    return mongo.client[MONGO_DB]
