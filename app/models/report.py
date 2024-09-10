from sqlalchemy import Column, Integer, String, DateTime, Boolean, func, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base

metadata = Base.metadata
class Report(Base):
    __tablename__ = 'report'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    query = Column(String(65535), nullable=False)
    path = Column(String(255), nullable=False)
    user = relationship('User', back_populates='report')

from app.models.user import User


