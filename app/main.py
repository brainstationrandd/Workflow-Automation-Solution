from typing import List
from fastapi import FastAPI, File, HTTPException, UploadFile, status, Request
from fastapi.responses import StreamingResponse
from fastapi.responses import JSONResponse
from pathlib import Path
import shutil


from fastapi.middleware.cors import CORSMiddleware
from utils.logger import logger
from utils.scheduler import scheduler
from app.services.email_service import scheduled_task
from apscheduler.triggers.cron import CronTrigger
from app.helpers.helper import http_error_handler
from fastapi.exceptions import RequestValidationError
from app.helpers.custom_exception_handler import validation_exception_handler
from fastapi.staticfiles import StaticFiles


app = FastAPI()

from app.endpoints import user_controller
from app.endpoints import admin_controller
from app.endpoints import document_controller
from app.endpoints import role_controller
from app.endpoints import user_role_controller
from app.endpoints import job_controller
from app.endpoints import elastic_search_controller
from app.endpoints import sort_and_review_controler
sessions = {}

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
import os
import atexit


app.include_router(user_controller.router, prefix="/api/user", tags=["User"])
app.include_router(admin_controller.router, prefix="/api/admin", tags=["Admin"])
app.include_router(document_controller.router, prefix="/api/document", tags=["Document"])
app.include_router(role_controller.router, prefix="/api/role", tags=["Role"])
app.include_router(user_role_controller.router, prefix="/api/user_role", tags=["UserRole"])
app.include_router(job_controller.router, prefix="/api/job", tags=["Job"])
app.include_router(elastic_search_controller.router, prefix="/api/elastic_search", tags=["ElasticSearch"])
app.include_router(sort_and_review_controler.router, prefix="/api/sort_and_review", tags=["SortAndReview"])


app.add_exception_handler(HTTPException, http_error_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)


# app.on_event("startu



# -----------------------------------------------
# UNCOMMENT THIS TO RUN SCHEDULER [FIX TIME]
# -----------------------------------------------
# scheduler.start()

# scheduler.add_job(scheduled_task, CronTrigger(minute='*/1', timezone='UTC'))

#Health Checker
@app.get("/")
async def health():
    logger.info("Health check requested")
    return {"Status": "Ok 201"}

# Define the directory where files will be saved
UPLOAD_DIRECTORY = Path("uploaded_files")

# Create the directory if it doesn't exist
if not UPLOAD_DIRECTORY.exists():
    UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)
    
@app.post("/upload/")
async def upload_files(files: List[UploadFile] = File(...)):
    saved_files = []
    
    for file in files:
        try:
            file_location = UPLOAD_DIRECTORY / file.filename

            # Ensure the file path exists, handling edge cases
            file_location.parent.mkdir(parents=True, exist_ok=True)
            
            # Save the uploaded file
            with file_location.open("wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            saved_files.append({"filename": file.filename, "location": str(file_location)})
        
        except Exception as e:
            # Handle any exceptions that occur during file saving
            raise HTTPException(status_code=500, detail=f"Failed to save file {file.filename}. Error: {str(e)}")
    
    return {"files": saved_files}