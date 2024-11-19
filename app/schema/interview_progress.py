from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.models.interview_progress import InterviewProgress  # Replace with actual import path

# class InterviewProgressCreate(BaseModel):
#     application_id: UUID
#     stage: str
#     notes: Optional[str] = None
#     scheduled_date: Optional[datetime] = None

# class InterviewProgressUpdate(BaseModel):
#     stage: Optional[str] = None
#     notes: Optional[str] = None
#     scheduled_date: Optional[datetime] = None
#     updated_at: Optional[datetime] = None
from app.models.interview_progress import InterviewStageEnum  # Replace with actual import path
from datetime import datetime, timedelta

class InterviewProgressCreate(BaseModel):
    application_id: UUID
    stage: InterviewStageEnum
    notes: Optional[str] = None
    scheduled_date: Optional[datetime] = None


class InterviewProgressUpdate(BaseModel):
    stage: Optional[InterviewStageEnum] = None
    notes: Optional[str] = None
    scheduled_date: Optional[datetime] = None
    updated_at: Optional[datetime] = None