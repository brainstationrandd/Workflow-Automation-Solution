from sqlalchemy import Column, Integer, String, DateTime, Boolean, func, ForeignKey, Text, Enum
from app.db import Base
import enum

metadata = Base.metadata

# Define the Enum values in Python
class JobStatus(enum.Enum):
    active = "active"
    archived = "archived"

class Job(Base):
    __tablename__ = 'job'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    end_time = Column(DateTime, nullable=True)
    status = Column(Enum(JobStatus), nullable=False, default=JobStatus.active)  # Enum column for status
    ended = Column(Boolean, default=False)

from app.models.user import User
