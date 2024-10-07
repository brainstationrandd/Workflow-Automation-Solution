from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, BackgroundTasks
from app.db import get_db
from app.schema.job import *
from app.services.job_service import *
from app.helpers.custom_exception_handler import *
# from app.repository.document_repository import DocumentRepository
from utils.logger import logger
from utils.helper import custom_response_handler
from app.schema.job import *



router = APIRouter()

@router.get("/")
async def get_all_jobs():
    try:
        jobs = await get_all_jobs_service()
        return custom_response_handler(200, "Jobs retrieved successfully", jobs)
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
        return custom_response_handler(201, "Job created successfully", new_job)
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/{job_id}")
async def get_job_by_id(job_id: int):
    try:
        job = await get_job_by_id_service(job_id)
        return custom_response_handler(200, "Job retrieved successfully", job)
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/user/{user_id}")
async def get_job_by_user_id(user_id: int):
    try:
        job = await get_job_by_user_id_service(user_id)
        return custom_response_handler(200, "Job retrieved successfully", job)
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
        return custom_response_handler(200, "Job updated successfully", job)
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
        return custom_response_handler(200, "Job deleted successfully", job)
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")