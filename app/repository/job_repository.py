from fastapi import HTTPException
from requests import Session
from utils.logger import logger
from app.models.job import Job
from app.db import engine, SessionLocal, Base, get_db
from app.schema.job import *

class JobRepository:
    @staticmethod
    async def get_all_jobs():
        db = SessionLocal()
        try:
            jobs = db.query(Job).all()
            return jobs
        except HTTPException as e:
            logger.info(f'An HTTP error occurred: \n {str(e)}')
            raise e
        finally:
            db.close()

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

    @staticmethod
    async def get_job_by_id(job_id: int):
        db = SessionLocal()
        try:
            job = db.query(Job).filter(Job.id == job_id).first()
            return job
        except HTTPException as e:
            logger.info(f'An HTTP error occurred: \n {str(e)}')
            raise e
        finally:
            db.close()

    @staticmethod
    async def update_job(job_id: int, job: JobUpdate):
        db = SessionLocal()
        try:
            db_job = db.query(Job).filter(Job.id == job_id).first()
            if not db_job:
                raise HTTPException(status_code=404, detail="Job not found")
            if(job.name):
                db_job.name = job.name
            if(job.description):
                db_job.description = job.description
            if(job.user_id):
                db_job.user_id = job.user_id
            db.commit()
            db.refresh(db_job)
            return db_job
        except HTTPException as e:
            logger.info(f'An HTTP error occurred: \n {str(e)}')
            raise e
        finally:
            db.close()

    @staticmethod
    async def delete_job(job_id):
        db = SessionLocal()
        try:
            db_job = db.query(Job).filter(Job.id == job_id).first()
            if not db_job:
                raise HTTPException(status_code=404, detail="Job not found")
            db.delete(db_job)
            db.commit()
            return db_job
        except HTTPException as e:
            logger.info(f'An HTTP error occurred: \n {str(e)}')
            raise e
        finally:
            db.close()