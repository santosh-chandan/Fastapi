from sqlalchemy.ext.asyncio import AsyncSession
from app.core.engine_psgl import async_sessionmaker
from app.chat.models import DocumentChunks

class IngestionService():

    # db: AsyncSession = Depends(get_db)    # it will not work here only part of fastapi req lifecycle

    async def save_as_vectors(self, sentences: list[str], db: AsyncSession):
        for chunk in sentences:
            # Need to implement Chuncking Strategies... using tokenizer of specific embedding model.
            dock_chunks = DocumentChunks(
                content = chunk,
                sorce = 'pdf'
            )
            db.add(dock_chunks)
        await db.commit()

    async def save_as_vectors_db(self, text: str):
        async with async_sessionmaker() as db:   # creates new DB session
            # starts transaction: success → COMMIT exception → ROLLBACK, session closes automatically
            async with db.begin():
                # use db
                pass

ingestionService = IngestionService()
