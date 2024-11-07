from sqlalchemy import Column, Integer, String, DateTime, Boolean, func, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.db import Base

metadata = Base.metadata

# SQLAlchemy model for job_applications table
class JobApplication(Base):
    __tablename__ = "job_applications"
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, nullable=False)
    path_cv = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    
    
from app.models.job_applications import JobApplication    