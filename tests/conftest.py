import pytest_asyncio
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from typing import AsyncGenerator
from app.core.engine_psgl import Base, get_db
from app.routes import rest_routes

TEST_DATABASE_URL = "postgresql+asyncpg://postgres:password@localhost:5432/fastapi_llm_test"

# ------------------------------
# FastAPI app fixture
# ------------------------------
@pytest_asyncio.fixture
async def app() -> AsyncGenerator[FastAPI, None]:
    app = FastAPI()
    app.include_router(rest_routes, prefix="/api")
    yield app

# ------------------------------
# Engine fixture (session-scoped)
# ------------------------------
@pytest_asyncio.fixture(scope="session")
async def engine() -> AsyncGenerator:
    engine = create_async_engine(TEST_DATABASE_URL, echo=True, future=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

# ------------------------------
# DB session fixture (per test)
# ------------------------------
@pytest_asyncio.fixture
async def db_session(engine) -> AsyncGenerator[AsyncSession, None]:
    """
    Provides a fresh AsyncSession per test using SAVEPOINT.
    Rollback automatically after test.
    """
    AsyncSessionLocal = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    async with AsyncSessionLocal() as session:
        async with session.begin_nested():  # <-- savepoint
            yield session
        # rollback automatically when exiting nested context

# ------------------------------
# Clean DB fixture (separate connection)
# ------------------------------
@pytest_asyncio.fixture(autouse=True)
async def clean_db(engine):
    """
    Truncate tables after each test using a fresh connection.
    """
    yield
    async with engine.begin() as conn:
        await conn.execute(text("TRUNCATE TABLE users RESTART IDENTITY CASCADE"))

# ------------------------------
# Async HTTP client fixture
# ------------------------------
@pytest_asyncio.fixture
async def client(app: FastAPI, db_session: AsyncSession) -> AsyncGenerator:
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    from httpx import AsyncClient
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
