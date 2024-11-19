from sqlalchemy import Column, String, DateTime, ForeignKey, Enum, Text, func, Integer,Float
from sqlalchemy.dialects.postgresql import UUID
import enum
import uuid
from app.db import Base

# Define the Enum values for match categories
class MatchCategory(enum.Enum):
    best_match = "best_match"
    medium_match = "medium_match"
    low_match = "low_match"
    shortlisted = "shortlisted"   # Replaces 'enlisted' for clarity
    miscellaneous = "miscellaneous"  # Corrects 'miscellenious'



class CVApplication(Base):
    __tablename__ = 'cv_applications'
    application_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    job_id = Column(Integer, ForeignKey('job.id', ondelete="CASCADE"), nullable=False)
    current_category = Column(Enum(MatchCategory), nullable=False)
    file_path = Column(String(500), nullable=False)
    email = Column(String(255), nullable=False)
    cv_hash = Column(String(64), nullable=False)  # 64 chars for SHA-256 hash or similar
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    cv_match_percentage = Column(Float, nullable=True)  # Percentage match (e.g., 87.5)
    key_strengths = Column(Text, nullable=True)  # Key strengths summary
    areas_of_concern = Column(Text, nullable=True)  # Areas of concern summary
    detailed_analysis = Column(Text, nullable=True)  # Detailed analysis text