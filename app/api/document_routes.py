from fastapi import APIRouter, UploadFile, File
import os
import uuid
from app.workers.tasks import process_document

router = APIRouter(prefix="/documents", tags=["Documents"])

UPLOAD_DIR = "app/storage/documents"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    file_id = str(uuid.uuid4())
    file_path = os.path.join(
        UPLOAD_DIR,
        f"{file_id}_{file.filename}"
    )

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    task = process_document.delay(file_path, file_id)

    return {
        "file_id": file_id,
        "filename": file.filename,
        "task_id": task.id,
        "status": "processing"
    }