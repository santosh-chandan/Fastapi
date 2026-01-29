from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.blog.service import postService
from app.auth.services import authService
from app.core.engine_psgl import get_db
from app.blog.schemas import CreatePost, SendPost
from app.user.models import User


blog_router = APIRouter(prefix='/v1/post', tags=['Posts'])


# Get post by id
@blog_router.get('/{id}', response_model=SendPost)
async def get_post(id: int, db: AsyncSession = Depends(get_db)):
    return await postService.get_post_by_id(id, db)


# Create post
@blog_router.post('/')
async def create_post(data: CreatePost, current_user: User = Depends(authService.get_current_user), db: AsyncSession = Depends(get_db)):
    return await postService.create_post(data, current_user, db)


# Get user post
@blog_router.get('/user/{id}')
async def get_user_posts(
    id: int,
    page = Query(1, ge=1),
    size = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    return await postService.get_user_posts(id, page, size, db)


# Get all posts
@blog_router.get('/me')
async def get_posts(
    limit: int = 10,
    cursor: int | None = None,
    current_usr: User = Depends(authService.get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await postService.get_user_post_cursor(current_usr.id, limit, cursor, db)

