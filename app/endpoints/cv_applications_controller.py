from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.models.cv_applications import CVApplication, MatchCategory  # Replace with actual import path
from app.db import get_db  # Replace with actual import path
from app.schema.cv_applications import CVApplicationCreate, CVApplicationUpdate  # Replace with actual import path
from utils.logger import logger
from app.models.cv_applications import CVApplication
from app.models.job import Job  
from sqlalchemy.sql import text
from app.schema.interview_progress import InterviewProgressCreate  # Replace with actual import path
from app.models.interview_progress import InterviewProgress, InterviewStageEnum  # Replace with actual import path

router = APIRouter()

def create_cvapplication(cv_application_data: dict, db: Session):
    try:
        # Create a new CV application instance
        db_cv_application = CVApplication(**cv_application_data)
        db.add(db_cv_application)
        db.commit()
        db.refresh(db_cv_application)
        return db_cv_application
    except Exception as e:
        logger.info(f"An error occurred while creating CV application: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create CV application")

@router.post("/cv_applications/")
async def create_cv_application(cv_application: CVApplicationCreate, db: Session = Depends(get_db)):
    try:
        db_cv_application = CVApplication(**cv_application.dict())
        db.add(db_cv_application)
        db.commit()
        db.refresh(db_cv_application)
        return db_cv_application
    except Exception as e:
        logger.info(f'An error occurred: {str(e)}')
        raise HTTPException(status_code=500, detail="Failed to create CV application")

@router.get("/cv_applications/")
async def get_all_cv_applications(db: Session = Depends(get_db)):
    try:
        cv_applications = db.query(CVApplication).all()
        return cv_applications
    except Exception as e:
        logger.info(f'An error occurred: {str(e)}')
        raise HTTPException(status_code=500, detail="Failed to fetch CV applications")

@router.get("/cv_applications/{application_id}")
async def get_cv_application_by_id(application_id: UUID, db: Session = Depends(get_db)):
    try:
        cv_application = db.query(CVApplication).filter(CVApplication.application_id == application_id).first()
        if not cv_application:
            raise HTTPException(status_code=404, detail="CV application not found")
        return cv_application
    except Exception as e:
        logger.info(f'An error occurred: {str(e)}')
        raise HTTPException(status_code=500, detail="Failed to fetch CV application")

# @router.put("/cv_applications/{application_id}")
# async def update_cv_application(application_id: UUID, cv_application: CVApplicationUpdate, db: Session = Depends(get_db)):
#     try:
#         db_cv_application = db.query(CVApplication).filter(CVApplication.application_id == application_id).first()
#         if not db_cv_application:
#             raise HTTPException(status_code=404, detail="CV application not found")
        
#         for key, value in cv_application.dict().items():
#             if value is not None:
#                 setattr(db_cv_application, key, value)
        
#         db.commit()
#         db.refresh(db_cv_application)
#         return db_cv_application
#     except Exception as e:
#         logger.info(f'An error occurred: {str(e)}')
#         raise HTTPException(status_code=500, detail="Failed to update CV application")

@router.put("/cv_applications/{application_id}")
async def update_cv_application(application_id: UUID, cv_application: CVApplicationUpdate, db: Session = Depends(get_db)):
    try:
        db_cv_application = db.query(CVApplication).filter(CVApplication.application_id == application_id).first()
        if not db_cv_application:
            raise HTTPException(status_code=404, detail="CV application not found")
        
        for key, value in cv_application.dict().items():
            if value is not None:
                setattr(db_cv_application, key, value)
        
        db.commit()
        db.refresh(db_cv_application)

        # If the current_category is updated to 'shortlisted', create a row in interview_progress
        if db_cv_application.current_category == MatchCategory.shortlisted:
            interview_progress = InterviewProgressCreate(
                application_id=application_id,
                stage=InterviewStageEnum.SCREENING,
                notes="Initial screening scheduled"
            )
            db_interview_progress = InterviewProgress(**interview_progress.dict())
            db.add(db_interview_progress)
            db.commit()
            db.refresh(db_interview_progress)

        return db_cv_application
    except Exception as e:
        logger.info(f'An error occurred: {str(e)}')
        raise HTTPException(status_code=500, detail="Failed to update CV application")



@router.delete("/cv_applications/{application_id}")
async def delete_cv_application(application_id: UUID, db: Session = Depends(get_db)):
    try:
        db_cv_application = db.query(CVApplication).filter(CVApplication.application_id == application_id).first()
        if not db_cv_application:
            raise HTTPException(status_code=404, detail="CV application not found")

        db.delete(db_cv_application)
        db.commit()
        return db_cv_application
    except Exception as e:
        logger.info(f'An error occurred: {str(e)}')
        raise HTTPException(status_code=500, detail="Failed to delete CV application")
    
    
@router.get("/jobs/applications")
def get_job_applications(db: Session = Depends(get_db)):
    """
    Fetch job applications grouped by job status and current category.
    """
    try:
        # Raw SQL query with text() wrapping
        results = db.execute(text("""
            SELECT
                j.status AS job_status,
                j.name AS job_title,
                j.id AS job_id,
                c.application_id AS application_uid,
                c.current_category,
                c.file_path,
                c.email,
                c.cv_match_percentage,
                c.key_strengths,
                c.areas_of_concern,
                c.detailed_analysis,
                c.created_at
            FROM
                job j
            JOIN
                cv_applications c ON j.id = c.job_id
            WHERE
                c.current_category != 'shortlisted'
            ORDER BY
                j.status, j.name, c.current_category,c.created_at DESC;
        """)).fetchall()

        # Initialize the data structure
        data = {"Active_Jobs": {}, "Archive_Jobs": {}}
       
        # Process data into the desired JSON format
        for row in results:
            job_status_key = "Active_Jobs" if row.job_status == "active" else "Archive_Jobs"
            job_title = row.job_title
            current_category = row.current_category
            
            # Ensure nested structure exists
            if job_title not in data[job_status_key]:
                data[job_status_key][job_title] = {
                    "best_match": [],
                    "medium_match": [],
                    "low_match": [],
                    "miscellaneous": []
                }
                
            # Append application details to the relevant category
            data[job_status_key][job_title][current_category].append({
                "job_id": row.job_id,
                "job_title": job_title,
                "email": row.email,
                "file_path": row.file_path,
                "application_uid": row.application_uid,
                "current_category": current_category,
                "cv_match_percentage": row.cv_match_percentage,
                "key_strengths": row.key_strengths,
                "areas_of_concern": row.areas_of_concern,
                "detailed_analysis": row.detailed_analysis,
                "created_at": row.created_at
            })
            
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")