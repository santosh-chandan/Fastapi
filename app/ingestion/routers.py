from fastapi import APIRouter, UploadFile, File, HTTPException
from uuid import uuid4
import shutil
import os

router = APIRouter(prefix="/v1/ingestion", tags=["Ingestion"])

INGEST_DIR = "storage/ingestion/processing"
os.makedirs(INGEST_DIR, exist_ok=True)

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    # Validate file type
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")

    # Generate safe unique filename
    pdf_id = f"{uuid4()}.pdf"
    file_path = os.path.join(INGEST_DIR, pdf_id)

    # Save file to disk
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Return immediately (async-friendly)
    return {
        "message": "File uploaded successfully",
        "pdf_id": pdf_id,
        "status": "queued_for_ingestion"
    }
