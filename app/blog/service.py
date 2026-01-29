from app.blog.models import Post
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.blog.schemas import CreatePost
from app.user.models import User
from app.core.exceptions import exceptions

class PostService():
    async def create_post(self, data: CreatePost, current_user: User, db: AsyncSession):
        post = Post(
            title= data.title,
            content= data.content,
            user_id= current_user.id
        )
        db.add(post)
        await db.commit()
        await db.refresh(post)
        return post

    async def get_post_by_id(self, id: int, db: AsyncSession):
        result = await db.execute(
            select(Post).where(Post.id == id)
        )
        post = result.scalar_one_or_none()
        if not post:
            raise exceptions.PostNotFound("Post doesn't exist.")

        return post

    # This is OFFSET-based pagination - LIMIT 10 OFFSET 10000
    async def get_user_posts(self, user_id, page, size, db: AsyncSession):
        result = await db.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()
        if not user:
            raise exceptions.UserNotFound("User does not exist.")
        
        result = await db.execute(
            select(Post)
            .where(Post.user_id == user_id)
            .order_by(Post.id.desc())
            .limit(size)
            .offset(page)
        )
        posts = result.scalars().all()

        total_post = await db.execute(
            select(func.count()).select_from(Post).where(Post.user_id == user_id)
        )
        total = total_post.scalar()

        return {
            "user_id": user_id,
            "page": page,
            "size": size,
            "posts": posts,
            "total": total,
            "pages": (total + size - 1) // size
        }

    async def get_user_post_cursor(self, user_id: int, limit: int, cursor: int | None, db: AsyncSession):
        
        query = select(Post).where(Post.id == user_id)

        if cursor:
            query.where(Post.id < cursor)
        
        query.order_by(Post.id.desc)
        query.limit(limit + 1)

        result = await db.execute(query)
        posts = result.scalars().all()

        has_more = len(posts) > limit
        if has_more:
            posts = posts[:-1]

        next_cursor = posts[:-1].id if posts else None

        return {
            "items": posts,
            "next_cursor": next_cursor,
            "has_more": has_more
        }


    async def get_all_posts(self):
        pass


    async def update_post(self):
        pass


    async def delete_post(self):
        pass


postService = PostService()
