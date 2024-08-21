from http.client import HTTPException
from app.schema.job import *
from app.models.job import Job
from app.repository.job_repository import JobRepository
from utils.logger import logger


async def get_all_jobs_service():
    try:
        jobs = await JobRepository.get_all_jobs()
        return jobs
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e

async def create_job_service(job: JobBase):
    try:
        db_job = await JobRepository.create_job(job)
        return db_job
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    

async def get_job_by_id_service(job_id):
    try:
        job = await JobRepository.get_job_by_id(job_id)
        return job
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    

async def update_job_service(job_id: int, job: JobUpdate):
    try:
        job = await JobRepository.update_job(job_id, job)
        return job
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    
async def delete_job_service(job_id):
    try:
        job = await JobRepository.delete_job(job_id)
        return job
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e