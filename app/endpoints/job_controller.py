from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, BackgroundTasks
from app.db import get_db
from app.schema.job import *
from app.services.job_service import *
from app.helpers.custom_exception_handler import *
# from app.repository.document_repository import DocumentRepository
from utils.logger import logger

router = APIRouter()

@router.get("/", response_model=List[JobBase])
async def get_all_jobs():
    try:
        jobs = await get_all_jobs_service()
        return jobs
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

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
    

@router.get("/{job_id}", response_model=JobBase)
async def get_job_by_id(job_id: int):
    try:
        job = await get_job_by_id_service(job_id)
        return job
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    

@router.put("/{job_id}")
async def update_job(job_id: int, job: JobUpdate):
    try:
        job = await update_job_service(job_id, job)
        return job
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
@router.delete("/{job_id}")
async def delete_job(job_id: int):
    try:
        job = await delete_job_service(job_id)
        return job
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")