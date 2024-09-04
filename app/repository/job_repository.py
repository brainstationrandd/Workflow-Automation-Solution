from fastapi import HTTPException
from requests import Session
from utils.logger import logger
from app.models.job import Job
from app.models.user import User
from app.db import engine, SessionLocal, Base, get_db
from app.schema.job import *
from datetime import datetime

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
    
    @staticmethod
    def get_expired_jobs():
        db = SessionLocal()
        now = datetime.now()
        try:
            jobs = db.query(Job.id).filter(Job.ended == False, Job.end_time < now).all()
            return jobs
        except HTTPException as e:
            logger.info(f'An HTTP error occurred: \n {str(e)}')
            raise e
        finally:
            db.close()

    @staticmethod
    def get_email_by_job_id(job_id: int):
        db = SessionLocal()
        try:
            user_email = db.query(User.email).join(Job, User.id == Job.user_id).filter(Job.id == job_id).first()
            if not user_email:
                logger.info(f"user email corresponding to {job_id} not found.")
                raise HTTPException(status_code=404, detail="User not found")
            return user_email
        except HTTPException as e:
            logger.info(f'An HTTP error occurred: \n {str(e)}')
            raise e
        finally:
            db.close()

    @staticmethod
    def get_user_by_job_id(job_id: int):
        db = SessionLocal()
        try:
            job = db.query(Job).filter(Job.id == job_id).first()
            return job.user_id
        except HTTPException as e:
            logger.info(f'An HTTP error occurred: \n {str(e)}')
            raise e
        finally:
            db.close()
