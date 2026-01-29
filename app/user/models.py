# app/user/model.py
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String
from app.core.engine_psgl import Base
from app.blog.models import Post

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    level: Mapped[str] = mapped_column(Integer, default=0)

    # ONE user → MANY posts
    posts: Mapped[list["Post"]] = relationship(back_populates="auther", cascade="all, delete")
        # It tells SQLAlchemy: 
            # When I do something to a User object, automatically do the same to its related Post objects. 
            # This happens at the ORM level, not SQL.
