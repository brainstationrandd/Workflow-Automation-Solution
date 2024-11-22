
from fastapi import HTTPException
from utils.logger import logger
from app.models.job import Job
from app.models.user import User
from app.db import SessionLocal
from app.schema.job import JobBase, JobUpdate
from datetime import datetime
from typing import List


class JobRepository:
    @staticmethod
    def get_all_jobs() -> List[Job]:
        try:
            with SessionLocal() as db:
                jobs = db.query(Job).filter(Job.ended == False).all()
                return jobs
        except Exception as e:
            logger.info(f'An error occurred: {str(e)}')
            raise HTTPException(status_code=500, detail="Failed to fetch jobs")

    @staticmethod
    def create_job(job: JobBase) -> Job:
        try:
            with SessionLocal() as db:
                db_job = Job(**job.dict())
                db.add(db_job)
                db.commit()
                db.refresh(db_job)
                return db_job
        except Exception as e:
            logger.info(f'An error occurred: {str(e)}')
            raise HTTPException(status_code=500, detail="Failed to create job")

    @staticmethod
    def get_job_by_id(job_id: int) -> Job:
        try:
            with SessionLocal() as db:
                job = db.query(Job).filter(Job.id == job_id, Job.ended == False).first()
                if not job:
                    raise HTTPException(status_code=404, detail="Job not found")
                return job
        except Exception as e:
            logger.info(f'An error occurred: {str(e)}')
            return HTTPException(status_code=500, detail="Failed to fetch job")

    @staticmethod
    def get_job_by_user_id(user_id: int) -> List[Job]:
        try:
            with SessionLocal() as db:
                jobs = db.query(Job).filter(Job.user_id == user_id, Job.ended == False).all()
                return jobs
        except Exception as e:
            logger.info(f'An error occurred: {str(e)}')
            raise HTTPException(status_code=500, detail="Failed to fetch jobs for user")

    @staticmethod
    def update_job(job_id: int, job: JobUpdate) -> Job:
        try:
            with SessionLocal() as db:
                db_job = db.query(Job).filter(Job.id == job_id, Job.ended == False).first()
                if not db_job:
                    raise HTTPException(status_code=404, detail="Job not found")
                
                # Update fields if they are provided in the request
                if job.name is not None:
                    db_job.name = job.name
                if job.description is not None:
                    db_job.description = job.description
                if job.status is not None:
                    db_job.status = job.status
                if job.end_time is not None:
                    db_job.end_time = job.end_time

                db.commit()
                db.refresh(db_job)
                return db_job
        except Exception as e:
            logger.info(f'An error occurred: {str(e)}')
            raise HTTPException(status_code=500, detail="Failed to update job")

    @staticmethod
    def delete_job(job_id: int) -> Job:
        try:
            with SessionLocal() as db:
                db_job = db.query(Job).filter(Job.id == job_id, Job.ended == False).first()
                if not db_job:
                    raise HTTPException(status_code=404, detail="Job not found")

                db.delete(db_job)
                db.commit()
                return db_job
        except Exception as e:
            logger.info(f'An error occurred: {str(e)}')
            raise HTTPException(status_code=500, detail="Failed to delete job")

    @staticmethod
    def get_expired_jobs() -> List[int]:
        now = datetime.now()
        try:
            with SessionLocal() as db:
                jobs = db.query(Job.id).filter(Job.ended == False, Job.end_time < now).all()
                return [job.id for job in jobs]
        except Exception as e:
            logger.info(f'An error occurred: {str(e)}')
            raise HTTPException(status_code=500, detail="Failed to fetch expired jobs")

    @staticmethod
    def get_email_by_job_id(job_id: int) -> str:
        try:
            with SessionLocal() as db:
                user_email = db.query(User.email).join(Job, User.id == Job.user_id).filter(Job.id == job_id, Job.ended == False).first()
                if not user_email:
                    raise HTTPException(status_code=404, detail="User not found for the job")
                return user_email[0]
                return user_email[0]
        except Exception as e:
            logger.info(f'An error occurred: {str(e)}')
            raise HTTPException(status_code=500, detail="Failed to fetch user email by job ID")

    @staticmethod
    def get_user_by_job_id(job_id: int) -> int:
        try:
            with SessionLocal() as db:
                job = db.query(Job).filter(Job.id == job_id).first()
                if not job:
                    raise HTTPException(status_code=404, detail="Job not found")
                return job.user_id
        except Exception as e:
            logger.info(f'An error occurred: {str(e)}')
            raise HTTPException(status_code=500, detail="Failed to fetch user by job ID")
