from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from app.db import get_db
from app.schema.job import *
from app.services.job_service import *
from app.helpers.custom_exception_handler import *
# from app.repository.document_repository import DocumentRepository
from utils.logger import logger
from utils.helper import custom_response_handler
from app.schema.job import *
from sqlalchemy.orm import Session



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

@router.get("/paginated")
async def get_jobs_with_pagination(offset: int = Query(0, ge=0), limit: int = Query(10, ge=1), db:Session = Depends(get_db)):
    """
    Get jobs with pagination.
    - offset: The number of items to skip before starting to collect the result set.
    - limit: The number of items to return.
    """
    try:
        jobs = await get_jobs_with_pagination_service(db, offset, limit)
        return custom_response_handler(200, "Jobs retrieved successfully", jobs)
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    

@router.get("/search")
async def find_jobs_by_name(name: str, db: Session = Depends(get_db)):
    """
    Find jobs by name (prefix and case insensitive).
    - name: The prefix of the job name to search for.
    """
    try:
        jobs = await find_jobs_by_name_service(db, name)
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
    

@router.get("/user/{user_id}/paginated")
async def get_jobs_by_user_id_with_pagination(user_id: int, offset: int = Query(0, ge=0), limit: int = Query(10, ge=1), db: Session = Depends(get_db)):
    """
    Get paginated jobs for a specific user by user ID.
    - user_id: The ID of the user.
    - offset: The number of items to skip before starting to collect the result set.
    - limit: The number of items to return.
    """
    try:
        jobs = await get_jobs_by_user_id_with_pagination_service(db, user_id, offset, limit)
        return custom_response_handler(200, "Jobs retrieved successfully", jobs)
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
    
    
 
 
@router.get("/user/{user_id}/search")
async def find_jobs_by_user_id_and_name(user_id: int, name: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    """
    Find jobs by name for a specific user (prefix and case insensitive).
    - user_id: The ID of the user.
    - name: The prefix of the job name to search for.
    """
    try:
        jobs = await find_jobs_by_user_id_and_name_service(db, user_id, name)
        return custom_response_handler(200, "Jobs retrieved successfully", jobs)
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")   

@router.get("/jobs/status/{status}")
async def get_jobs_by_status(status: str, db: Session = Depends(get_db)):
    try:
        jobs = db.query(Job).filter(Job.status == status).all()
        if not jobs:
            raise HTTPException(status_code=404, detail=f"No jobs found with status {status}")
        return jobs
    except Exception as e:
        logger.info(f'An error occurred: {str(e)}')
        raise HTTPException(status_code=500, detail="Failed to fetch jobs by status")