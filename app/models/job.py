from sqlalchemy import Column, Integer, String, DateTime, Boolean, func, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base

metadata = Base.metadata

class Job(Base):
    __tablename__ = 'job'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    description = Column(String(65535), nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    end_time = Column(DateTime, nullable=True)
    ended = Column(Boolean, default=False)

from app.models.user import User
