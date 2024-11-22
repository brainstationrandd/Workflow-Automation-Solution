# from http.client import HTTPException
# from app.schema.job import *
# from app.models.job import Job
# from app.repository.job_repository import JobRepository
# from utils.logger import logger
# from sqlalchemy.orm import Session


# async def get_all_jobs_service():
#     try:
#         jobs = await JobRepository.get_all_jobs()
#         return jobs
#     except HTTPException as e:
#         logger.info(f'An HTTP error occurred: \n {str(e)}')
#         raise e

# async def create_job_service(job: JobBase):
#     try:
#         db_job = await JobRepository.create_job(job)
#         return db_job
#     except HTTPException as e:
#         logger.info(f'An HTTP error occurred: \n {str(e)}')
#         raise e
    

# async def get_job_by_id_service(job_id):
#     try:
#         job = await JobRepository.get_job_by_id(job_id)
#         return job
#     except HTTPException as e:
#         logger.info(f'An HTTP error occurred: \n {str(e)}')
#         raise e

# async def get_jobs_with_pagination_service(db: Session, offset: int, limit: int):
#     try:
#         jobs = db.query(Job).offset(offset).limit(limit).all()
#         return jobs
#     except Exception as e:
#         logger.error(f'An error occurred while fetching jobs with pagination: \n {str(e)}')
#         raise HTTPException(status_code=500, detail="An error occurred while fetching jobs with pagination")


# async def find_jobs_by_name_service(db: Session, name: str):
#     try:
#         jobs = db.query(Job).filter(Job.name.ilike(f'{name}%')).all()
#         return jobs
#     except Exception as e:
#         logger.error(f'An error occurred while fetching jobs by name: \n {str(e)}')
#         raise HTTPException(status_code=500, detail="An error occurred while fetching jobs by name")

# async def get_job_by_user_id_service(user_id):
#     try:
#         job = await JobRepository.get_job_by_user_id(user_id)
#         return job
#     except HTTPException as e:
#         logger.info(f'An HTTP error occurred: \n {str(e)}')
#         raise e
    

# async def update_job_service(job_id: int, job: JobUpdate):
#     try:
#         job = await JobRepository.update_job(job_id, job)
#         return job
#     except HTTPException as e:
#         logger.info(f'An HTTP error occurred: \n {str(e)}')
#         raise e
    
# async def delete_job_service(job_id):
#     try:
#         job = await JobRepository.delete_job(job_id)
#         return job
#     except HTTPException as e:
#         logger.info(f'An HTTP error occurred: \n {str(e)}')
#         raise e
    
    

# async def get_jobs_by_user_id_with_pagination_service(db: Session, user_id: int, offset: int, limit: int):
#     try:
#         jobs = db.query(Job).filter(Job.user_id == user_id).offset(offset).limit(limit).all()
#         return jobs
#     except Exception as e:
#         logger.error(f'An error occurred while fetching jobs by user ID with pagination: \n {str(e)}')
#         raise HTTPException(status_code=500, detail="An error occurred while fetching jobs by user ID with pagination")    
    
    

# async def find_jobs_by_user_id_and_name_service(db: Session, user_id: int, name: str):
#     try:
#         jobs = db.query(Job).filter(Job.user_id == user_id, Job.name.ilike(f'{name}%')).all()
#         return jobs
#     except Exception as e:
#         logger.error(f'An error occurred while fetching jobs by user ID and name: \n {str(e)}')
#         raise HTTPException(status_code=500, detail="An error occurred while fetching jobs by user ID and name")    


from fastapi import HTTPException
from app.schema.job import *
from app.models.job import Job
from app.repository.job_repository import JobRepository
from utils.logger import logger
from sqlalchemy.orm import Session


# Helper function to handle errors
def handle_exception(e: Exception, message: str, status_code: int = 500):
    logger.error(f'{message}: {str(e)}')
    raise HTTPException(status_code=status_code, detail=message)


async def get_all_jobs_service():
    try:
        jobs = JobRepository.get_all_jobs()  # Removed 'await' as it is synchronous
        return jobs
    except Exception as e:
        handle_exception(e, "An error occurred while fetching all jobs")


async def create_job_service(job: JobBase):
    try:
        db_job = JobRepository.create_job(job)  # Removed 'await' as it is synchronous
        return db_job
    except Exception as e:
        handle_exception(e, "An error occurred while creating the job")


async def get_job_by_id_service(job_id: int):
    try:
        job = JobRepository.get_job_by_id(job_id)  # Removed 'await' as it is synchronous
        return job
    except Exception as e:
        handle_exception(e, "An error occurred while fetching the job by ID")


async def get_jobs_with_pagination_service(db: Session, offset: int, limit: int):
    try:
        jobs = db.query(Job).filter(Job.ended == False).offset(offset).limit(limit).all()
        return jobs
    except Exception as e:
        handle_exception(e, "An error occurred while fetching jobs with pagination")


async def find_jobs_by_name_service(db: Session, name: str):
    try:
        jobs = db.query(Job).filter(Job.name.ilike(f'{name}%')).all()
        return jobs
    except Exception as e:
        handle_exception(e, "An error occurred while fetching jobs by name")


async def get_job_by_user_id_service(user_id: int):
    try:
        jobs = JobRepository.get_job_by_user_id(user_id)  # Removed 'await' as it is synchronous
        return jobs
    except Exception as e:
        handle_exception(e, "An error occurred while fetching jobs by user ID")


async def update_job_service(job_id: int, job: JobUpdate):
    try:
        updated_job = JobRepository.update_job(job_id, job)  # Removed 'await' as it is synchronous
        return updated_job
    except Exception as e:
        handle_exception(e, "An error occurred while updating the job")


async def delete_job_service(job_id: int):
    try:
        job = JobRepository.delete_job(job_id)  # Removed 'await' as it is synchronous
        return job
    except Exception as e:
        handle_exception(e, "An error occurred while deleting the job")


async def get_jobs_by_user_id_with_pagination_service(db: Session, user_id: int, offset: int, limit: int):
    try:
        jobs = db.query(Job).filter(Job.user_id == user_id).offset(offset).limit(limit).all()
        return jobs
    except Exception as e:
        handle_exception(e, "An error occurred while fetching jobs by user ID with pagination")


async def find_jobs_by_user_id_and_name_service(db: Session, user_id: int, name: str):
    try:
        jobs = db.query(Job).filter(Job.user_id == user_id, Job.name.ilike(f'{name}%')).all()
        return jobs
    except Exception as e:
        handle_exception(e, "An error occurred while fetching jobs by user ID and name")
