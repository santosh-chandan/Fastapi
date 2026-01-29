# main.py
from fastapi import FastAPI
import app.routes as routes
from contextlib import asynccontextmanager
from app.core.engine_psgl import engine, Base
from app.core.engine_mongo import connect_mongo, close_mongo
from app.core.exceptions.exceptions import UserNotFound, UserAlreadyExist
from app.core.exceptions.exception_handlers import user_not_found_handler, user_already_exist

# Lifspan Event
@asynccontextmanager
async def lifespan(app: FastAPI):   # actually passing Fastapi reference as parameter -> Allows access to app.state.*
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)   # remove for production and use alembic
    print("Table are created.")

    await connect_mongo()

    yield   # 👈 app runs here

    # Shutdown
    await engine.dispose()
    await close_mongo()

# Fastapi App with Lifespan
app = FastAPI(lifespan=lifespan)

app.add_exception_handler(UserNotFound, user_not_found_handler)
app.add_exception_handler(UserAlreadyExist, user_already_exist)

# Rest API
app.include_router(routes.rest_routes, prefix='/api')

# Graphql API
app.include_router(routes.graphql_routes, prefix='/graphql')

# Streaming API
app.include_router(routes.stream_routes, prefix='/stream')

# WebSocket API
app.include_router(routes.websocket_routes, prefix='/ws')

# Home Page
@app.get('/')
def get_root():
    return "Hello fastapi"
