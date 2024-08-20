from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, BackgroundTasks
from app.db import get_db
from app.schema.job import *
from app.services.job_service import *
from app.helpers.custom_exception_handler import *
# from app.repository.document_repository import DocumentRepository
from utils.logger import logger

router = APIRouter()

@router.post("/create-job/")
async def create_job(job: JobBase):
    try:
        new_job = await create_job_service(job)
        return new_job
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")