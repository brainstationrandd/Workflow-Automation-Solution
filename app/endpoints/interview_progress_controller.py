from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.models.interview_progress import InterviewProgress  # Replace with actual import path
from app.db import get_db  # Replace with actual import path
from app.schema.interview_progress import InterviewProgressCreate, InterviewProgressUpdate  # Replace with actual import path
from utils.logger import logger
from sqlalchemy.sql import text
from pydantic import BaseModel

router = APIRouter()

@router.post("/interview_progress/")
async def create_interview_progress(interview_progress: InterviewProgressCreate, db: Session = Depends(get_db)):
    try:
        db_interview_progress = InterviewProgress(**interview_progress.dict())
        db.add(db_interview_progress)
        db.commit()
        db.refresh(db_interview_progress)
        return db_interview_progress
    except Exception as e:
        logger.info(f'An error occurred: {str(e)}')
        raise HTTPException(status_code=500, detail="Failed to create interview progress")

@router.get("/interview_progress/")
async def get_all_interview_progress(db: Session = Depends(get_db)):
    try:
        interview_progresses = db.query(InterviewProgress).all()
        return interview_progresses
    except Exception as e:
        logger.info(f'An error occurred: {str(e)}')
        raise HTTPException(status_code=500, detail="Failed to fetch interview progress entries")

@router.get("/interview_progress/{progress_id}")
async def get_interview_progress_by_id(progress_id: UUID, db: Session = Depends(get_db)):
    try:
        interview_progress = db.query(InterviewProgress).filter(InterviewProgress.progress_id == progress_id).first()
        if not interview_progress:
            raise HTTPException(status_code=404, detail="Interview progress not found")
        return interview_progress
    except Exception as e:
        logger.info(f'An error occurred: {str(e)}')
        raise HTTPException(status_code=500, detail="Failed to fetch interview progress entry")

@router.put("/interview_progress/{progress_id}")
async def update_interview_progress(progress_id: UUID, interview_progress: InterviewProgressUpdate, db: Session = Depends(get_db)):
    try:
        db_interview_progress = db.query(InterviewProgress).filter(InterviewProgress.progress_id == progress_id).first()
        if not db_interview_progress:
            raise HTTPException(status_code=404, detail="Interview progress not found")
        
        for key, value in interview_progress.dict().items():
            if value is not None:
                setattr(db_interview_progress, key, value)
        
        db.commit()
        db.refresh(db_interview_progress)
        return db_interview_progress
    except Exception as e:
        logger.info(f'An error occurred: {str(e)}')
        raise HTTPException(status_code=500, detail="Failed to update interview progress")

@router.delete("/interview_progress/{progress_id}")
async def delete_interview_progress(progress_id: UUID, db: Session = Depends(get_db)):
    try:
        db_interview_progress = db.query(InterviewProgress).filter(InterviewProgress.progress_id == progress_id).first()
        if not db_interview_progress:
            raise HTTPException(status_code=404, detail="Interview progress not found")

        db.delete(db_interview_progress)
        db.commit()
        return db_interview_progress
    except Exception as e:
        logger.info(f'An error occurred: {str(e)}')
        raise HTTPException(status_code=500, detail="Failed to delete interview progress")
    
    

@router.get("/jobs/applications/{job_id}")
def get_job_applications_with_interviews_flat(job_id: int, db: Session = Depends(get_db)):
    """
    Fetch job applications with associated interview progress details for a specific job ID.
    Return a flat JSON list for each application and its associated interview details.
    """
    try:
        # SQL query to fetch job applications and interview progress
        results = db.execute(text("""
            SELECT
                j.id AS job_id,
                j.name AS job_title,
                j.status AS job_status,
                c.application_id AS application_uid,
                c.current_category,
                c.file_path,
                c.email,
                c.cv_match_percentage,
                c.key_strengths,
                c.areas_of_concern,
                c.detailed_analysis,
                ip.progress_id,
                ip.stage,
                ip.notes AS interview_notes,
                ip.scheduled_date AS interview_scheduled_date,
                ip.updated_at AS interview_updated_at,
                ip.created_at AS interview_created_at
            FROM
                job j
            JOIN
                cv_applications c ON j.id = c.job_id
            JOIN
                interview_progress ip ON c.application_id = ip.application_id
            WHERE
                j.id = :job_id
            ORDER BY
                j.status, c.current_category, ip.stage;
        """), {"job_id": job_id}).fetchall()

        # Process data into a flat JSON list
        data = []
        for row in results:
            # Combine job, application, and interview details into one object
            data.append({
                "job_id": row.job_id,
                "job_title": row.job_title,
                "job_status": row.job_status,
                "application_uid": row.application_uid,
                "current_category": row.current_category,
                "file_path": row.file_path,
                "email": row.email,
                "cv_match_percentage": row.cv_match_percentage,
                "key_strengths": row.key_strengths,
                "areas_of_concern": row.areas_of_concern,
                "detailed_analysis": row.detailed_analysis,
                "progress_id": row.progress_id,
                "interview_stage": row.stage,
                "interview_notes": row.interview_notes,
                "interview_scheduled_date": row.interview_scheduled_date,
                "interview_updated_at": row.interview_updated_at,
                "interview_created_at": row.interview_created_at
            })

        return data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

class UpdateNotes(BaseModel):
    notes: str
    application_id: UUID

@router.post("/notes")
def append_notes_by_application_id(updatenote:UpdateNotes, db: Session = Depends(get_db)):
    """
    Append notes to the interview progress entry for a specific application ID.
    """
    try:
        notes = updatenote.notes
        application_id = updatenote.application_id
        # Fetch the interview progress entry for the application
        interview_progress = db.query(InterviewProgress).filter(InterviewProgress.application_id == application_id).first()
        if not interview_progress:
            raise HTTPException(status_code=404, detail="Interview progress not found")

        # Append the new notes to the existing notes
        interview_progress.notes = f"{notes}"
        db.commit()
        db.refresh(interview_progress)
        return interview_progress

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to append notes: {str(e)}")
def stage_update(stage: str, application_id: UUID, scheduled_date: str, db: Session):
    """
    Update the interview stage and scheduled date for a specific application ID.
    """
     # Format the local date to store in the database (as ISO format without timezone info)
    formatted_date = scheduled_date.strftime("%Y-%m-%d %H:%M:%S")
        
        # Debug: Print formatted_date before saving
    print("Formatted scheduled_date_local for database:", formatted_date)
        
    # Fetch the interview progress entry for the application
    interview_progress = db.query(InterviewProgress).filter(InterviewProgress.application_id == application_id).first()
    if not interview_progress:
        raise HTTPException(status_code=404, detail="Interview progress not found")

    # Update the interview stage and scheduled date
    interview_progress.stage = stage
    interview_progress.scheduled_date = formatted_date
    db.commit()
    db.refresh(interview_progress)
    return interview_progress

def append_note_by_appication_uuid(notes: str, application_id: UUID, db: Session):
    """
    Append notes to the interview progress entry for a specific application ID.
    """
    # Fetch the interview progress entry for the application
    interview_progress = db.query(InterviewProgress).filter(InterviewProgress.application_id == application_id).first()
    if not interview_progress:
        raise HTTPException(status_code=404, detail="Interview progress not found")

    # Append the new notes to the existing notes
    interview_progress.notes+=f"\n{notes}"
    db.commit()
    db.refresh(interview_progress)
    return interview_progress
