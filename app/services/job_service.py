from http.client import HTTPException
from app.schema.job import JobBase
from app.models.job import Job
from app.repository.job_repository import JobRepository
from utils.logger import logger


async def create_job_service(job: JobBase):
    try:
        db_job = await JobRepository.create_job(job)
        return db_job
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e