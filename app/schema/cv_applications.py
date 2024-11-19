from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.models.cv_applications import MatchCategory  # Replace with actual import path

class CVApplicationCreate(BaseModel):
    job_id: int
    current_category: MatchCategory
    file_path: str
    cv_hash: str
    cv_match_percentage: Optional[float] = None
    key_strengths: Optional[str] = None
    areas_of_concern: Optional[str] = None
    detailed_analysis: Optional[str] = None
    

class CVApplicationUpdate(BaseModel):
    job_id: Optional[int] = None
    current_category: Optional[MatchCategory] = None
    file_path: Optional[str] = None
    updated_at: Optional[datetime] = None
    cv_match_percentage: Optional[float] = None
    key_strengths: Optional[str] = None
    areas_of_concern: Optional[str] = None
    detailed_analysis: Optional[str] = None
    
    