import shutil
from datetime import datetime
import zipfile
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.params import Depends
import os

from typing_extensions import Optional

import oath2
from schemas import UserResponse
from user import router as user_router
from auth import router as auth_router
from database import get_db
from models import LogEntry

app = FastAPI()

app.include_router(user_router)
app.include_router(auth_router)


@app.post("/upload")
async def upload_file(file: UploadFile, db=Depends(get_db)):
    filename = file.filename
    file_path = f"logs/{filename}"
    os.makedirs("logs", exist_ok=True)

    if filename in os.listdir("logs"):
        raise HTTPException(
            status_code=409, detail="The file with the same name already exists"
        )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    if zipfile.is_zipfile(file_path):
        extract_dir = os.path.join("logs", filename.removesuffix(".zip"))

        os.makedirs(extract_dir, exist_ok=True)

        with zipfile.ZipFile(file_path, "r") as zip_ref:
            zip_ref.extractall(extract_dir)

        os.remove(file_path)
        file_path = extract_dir

    if os.path.isdir(file_path):
        for extracted_file in os.listdir(file_path):
            extracted_file_path = os.path.join(file_path, extracted_file)

            if os.path.isfile(extracted_file_path):

                with open(extracted_file_path, "r") as f:
                    content = f.read()

                log_entry = LogEntry(filename=extracted_file, content=content)

                db.add(log_entry)


    else:
        with open(file_path, "r") as f:
            content = f.read()

        log_entry = LogEntry(filename=filename, content=content)

        db.add(log_entry)

    db.commit()

    return {"success"}


@app.get("/logs")
async def get_logs(
    db=Depends(get_db),
    search_word: Optional[str] = "",
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    current_user: UserResponse = Depends(oath2.get_current_user_id),
):
    query = db.query(LogEntry)

    if start_time:
        query = query.filter(LogEntry.timestamp >= start_time)
    if end_time:
        query = query.filter(LogEntry.timestamp <= end_time)
    if search_word:
        query = query.filter(LogEntry.content.contains(search_word))

    logs = query.all()
    return {"logs": logs}
