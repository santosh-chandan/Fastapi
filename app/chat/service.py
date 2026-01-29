from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.engine_mongo import get_database
from app.core.embeddings.hf import embed_text
from app.chat.models import DocumentChunks
from app.core.llm.openai import stream_llm

# Mongo collection
COLLECTION = 'chat_history'


# -----------------------------------------------
# Streaming: LLM Chat Generator
# -----------------------------------------------
async def stream_chat(question: str, db: AsyncSession):
    yield "Data connnected"

    # Local CPU embedding
    embedded_question = embed_text(question)

    # pgvector search
    docs = get_similar_chunks(db, embedded_question, limit=3)

    # Build context for RAG
    context = "\n".join([doc.content for doc in docs])

    prompt = f"""
    Context:
    {context}

    Question:
    {question}
    """

    # Stream LLM response token-by-token
    async for token in stream_llm(prompt):
        yield f"data: {token}\n\n"

    # Save final conversation to Mongo
    # MongoDB is schema-less
    await save_message({
        "question": question,
        "context": context,
        "source": "rag"
    })

    yield "data: [DONE]\n\n"


# What YOU send to LLM
# Context:
# (chunk 1)
# (chunk 2)

# Question:
# (user question)

# What USER sees
# User types: "What is HNSW?"
# User receives: "HNSW is a graph-based index..."

# -----------------------------------------------
# Search Vecor Query
# -----------------------------------------------
async def get_similar_chunks(db: AsyncSession, embeddings: list[float], limit: int):
    result = await db.execute(
        select(DocumentChunks)
        .order_by(DocumentChunks.embedding_vector.cosine_distance(embeddings))
        .limit(limit)
    )
    return result.scalars().all()


# -----------------------------------------------
# Save Message
# -----------------------------------------------
async def save_message(data: dict):
    db = get_database()
    document = {
        **data,
        'created_at': datetime.now()
    }
    result = await db[COLLECTION].insert_one(document)
    document['id'] = str(result.inserted_id)
    return document
