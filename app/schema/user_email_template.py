from pydantic import BaseModel
from typing import Optional

class UserEmailTemplateCreate(BaseModel):
    user_id: int
    screening_template: str
    technical_template: str
    hr_template: str
    final_template: str
    offered_template: str
    rejected_template: str
    accepted_template: str

class UserEmailTemplateUpdate(BaseModel):
    screening_template: Optional[str] = None
    technical_template: Optional[str] = None
    hr_template: Optional[str] = None
    final_template: Optional[str] = None
    offered_template: Optional[str] = None
    rejected_template: Optional[str] = None
    accepted_template: Optional[str] = None