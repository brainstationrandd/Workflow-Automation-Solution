from sqlalchemy import Column, Integer, String, DateTime, Boolean, func, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base

metadata = Base.metadata

class Role(Base):
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(255), nullable=False)
    user_role = relationship('User_role', back_populates='role')

from app.models.user_role import User_role