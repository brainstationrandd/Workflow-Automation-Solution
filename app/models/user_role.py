from sqlalchemy import Column, Integer, String, DateTime, Boolean, func, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base

metadata = Base.metadata

class User_role(Base):
    __tablename__ = 'user_role'
    id = Column(Integer, primary_key=True, nullable=False)
    role_id = Column(Integer, ForeignKey('role.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    role = relationship('Role', back_populates='user_role')
    user = relationship('User', back_populates='user_role')


from app.models.role import Role
from app.models.user import User


