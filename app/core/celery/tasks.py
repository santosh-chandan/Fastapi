import os
import shutil
import asyncio
from pypdf import PdfReader
from app.core.celery.celery_app import celery_app
from app.ingestion.services import ingestionService
from filelock import FileLock, Timeout 
from app.core.engine_psgl import get_db

INGEST_DIR = 'storage/ingestion/processing'
PROCESSED_DIR = 'storage/ingestion/processed'
FAILED_DIR = 'storage/ingestion/failed'

# Celery cannot run async tasks
# We manually create an event loop
@celery_app.task('ingest_pdfs')
def get_ingestion_pdfs():
    """
    Celery entry point (SYNC)
    """
    asyncio.run(_ingestion_pdfs)

async def _ingestion_pdfs():

    # ensure directories exist
    os.makedirs(INGEST_DIR, exist_ok=True)
    os.makedirs(FAILED_DIR, exist_ok=True)

    for filename in os.listdir(INGEST_DIR):
        if not filename.endswith('.pdf'):
            continue
        
        file_path = os.path.join(INGEST_DIR, filename)
        lock_file = f"/temp/{filename}.lock"
        lock = FileLock(lock_file, timeout=1)   # file is locking here
        try:
            # 🔐 Prevent double ingestion
            with lock:
                # Lock file: - It will create .lock in temp folder then other process first check in temp/ then.
                reader = PdfReader(file_path)
                text = ''
                for page in reader.pages:
                    text += page.extract_text() or ''

                # manually create db connection (No Depends)
                # here for loop first call to start db and yield will stop
                # once resposne back from service class then again loop run and then with: close db session.
                async for db in get_db():
                    await ingestionService.save_as_vectors(text, db)

                shutil.move(file_path, os.path.join(PROCESSED_DIR, filename))
        
        except Timeout:
            continue

        except Exception as e:
            shutil.move(file_path, os.path.join(FAILED_DIR, filename))
            raise e
