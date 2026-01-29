# app/core/database.py
from app.core.config import PG_DB_URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


engine = create_async_engine(
    PG_DB_URL,
    pool_size=10,
    max_overflow=20,
    echo=True
)

# Create tables - engine.begin()
AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False
)

# 👉 get_db() is for CRUD, not DDL (schema creation)
async def get_db():
    async with AsyncSessionLocal() as session:  # a real DB connection created
        yield session
