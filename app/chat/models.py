from app.core.engine_psgl import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text, DateTime
from pgvector.sqlalchemy import Vector
from typing import Optional
from sqlalchemy.sql import func

class DocumentChunks(Base):
    __tablename__ = "document_chunks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    content: Mapped[str] = mapped_column(Text, nullable=False)

    # pgvector embedding
    embedding_vector: Mapped[list[float]] = mapped_column(
        Vector(384),
        nullable=False
    )

    source: Mapped[Optional[str]] = mapped_column(Text)
    document_id: Mapped[Optional[str]] = mapped_column(Text)

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
