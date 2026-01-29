"""add hnsw index for document_chunks

Revision ID: c9002a4d090d
Revises: ded05c0da8bd
Create Date: 2026-01-26 15:25:09.531819

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c9002a4d090d'
down_revision: Union[str, Sequence[str], None] = 'ded05c0da8bd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Ensure pgvector extension exists
    op.execute("CREATE EXTENSION IF NOT EXISTS vector;")

    # Create HNSW index for cosine similarity search
    op.execute("""
        CREATE INDEX IF NOT EXISTS idx_document_chunks_embedding_hnsw
        ON document_chunks
        USING hnsw (embedding_vector vector_cosine_ops)
        WITH (m = 16, ef_construction = 200);
    """)


def downgrade() -> None:
    """Downgrade schema."""

    # Drop HNSW index
    op.execute("""
        DROP INDEX IF EXISTS idx_document_chunks_embedding_hnsw;
    """)
