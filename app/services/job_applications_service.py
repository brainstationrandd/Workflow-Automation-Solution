from sqlalchemy.orm import Session
from app.models.job_applications import JobApplication
from sqlalchemy.exc import SQLAlchemyError


def store_job_application(job_id: int, path_cv: str, email: str, db: Session):
    try:
        # Create and add the job application record
        job_application = JobApplication(job_id=job_id, path_cv=path_cv, email=email)
        db.add(job_application)
        db.commit()
        db.refresh(job_application)
        return job_application
    except SQLAlchemyError as e:
        # Roll back the transaction if there is an error
        db.rollback()
        print(f"Error occurred: {e}")
        return None

def get_all_job_application_by_job_id(job_id: int, db: Session):
    try:
        job_applications = db.query(JobApplication).filter(JobApplication.job_id == job_id).all()
        return job_applications
    except SQLAlchemyError as e:    
        print(f"Error occurred: {e}")
        return None
    
    