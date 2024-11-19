from sqlalchemy import Column, String, Text, ForeignKey, Enum, DateTime, func,TIMESTAMP,CheckConstraint
import enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base

class InterviewStageEnum(str, enum.Enum):
    SCREENING = "screening"
    TECHNICAL = "technical"
    HR = "hr"
    FINAL = "final"
    OFFERED = "offered"
    REJECTED = "rejected"
    ACCEPTED = "accepted"

class InterviewProgress(Base):
    __tablename__ = "interview_progress"

    progress_id = Column(UUID(as_uuid=True), primary_key=True, default=func.gen_random_uuid())
    application_id = Column(UUID(as_uuid=True), ForeignKey("cv_applications.application_id", ondelete="CASCADE"), nullable=False)
    stage = Column(Enum(InterviewStageEnum), nullable=False)
    notes = Column(Text)
    scheduled_date = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())
    created_at = Column(TIMESTAMP, default=func.now())