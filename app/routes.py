from fastapi import APIRouter
from strawberry.fastapi import GraphQLRouter
from app.core.gql_context import context
from app.schema import schema
from app.user.v1.routers import router as user_router
from app.chat.routers import chat_router
from app.notification.routers import notification_router


# REST API router
rest_routes = APIRouter()
rest_routes.include_router(user_router)


# Streaming API router
# Server-Sent-Event OR HTTP Streaming
stream_routes = APIRouter()
stream_routes.include_router(chat_router)


# WebSocket API router
websocket_routes = notification_router

# graphql router
graphql_routes = GraphQLRouter(
    schema=schema, 
    context_getter=context
    )
