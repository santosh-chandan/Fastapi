from app.core.engine_psgl import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey, DateTime
from datetime import datetime


class Post(Base):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"), nullable=False)

    # MANY posts → ONE user
    # It is an ORM-level relationship, not a database column.
    auther = relationship('User', back_populates='posts')   # ORM sets user_id automatically
        # 'posts' - in this column is matching the same relattion column name in User table.

    images = relationship('PostImage', back_populates='post', cascade="all, delete-orphan")

    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True)

class PostImage(Base):
    __tablename__ = 'post_images'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    image_path: Mapped[str] = mapped_column(str(255), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id', ondelete="CASCADE"), nullable=False)

    post = relationship('Post', back_populates='images')
    # 'images' - in this column is matching the same relattion column name in Post table.
        # Why is it called "images"?
            # Because it’s a collection.
            # post.images   # → list[PostImage]
