from sqlalchemy import Column, Integer, String, DateTime, Boolean, func, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base

class report(Base):
    __tablename__ = 'report'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    query = Column(String(255), nullable=False)
    path = Column(String(255), nullable=False)
    user = relationship('user', back_populates='report_collection')
