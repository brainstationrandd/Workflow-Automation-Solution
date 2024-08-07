from sqlalchemy import Column, Integer, String, DateTime, Boolean, func, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base

class Metatag(Base):
    __tablename__ = 'metatag'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(255), nullable=False)
    document_metatag_collection = relationship('document_metatag', back_populates='metatag')
