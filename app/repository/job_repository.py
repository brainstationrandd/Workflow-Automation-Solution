from fastapi import HTTPException
from requests import Session
from utils.logger import logger
from app.models.job import Job
from app.db import engine, SessionLocal, Base, get_db
from app.schema.job import JobBase

class JobRepository:
    @staticmethod
    async def create_job(job: JobBase):
        db = SessionLocal()
        try:
            db_job = Job(**job.model_dump())
            db.add(db_job)
            db.commit()
            db.refresh(db_job) 
            return db_job
        except HTTPException as e:
            logger.info(f'An HTTP error occurred: \n {str(e)}')
            raise e
        finally:
            db.close()