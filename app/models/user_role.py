from sqlalchemy import Column, Integer, String, DateTime, Boolean, func, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base

class User_role(Base):
    __tablename__ = 'user_role'
    id = Column(Integer, primary_key=True, nullable=False)
    role_id = Column(Integer, ForeignKey('role.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    role = relationship('role', back_populates='user_role_collection')
    user = relationship('user', back_populates='user_role_collection')
