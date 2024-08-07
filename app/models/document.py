from sqlalchemy import Column, Integer, String, DateTime, Boolean, func, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base

class Document(Base):
    __tablename__ = 'document'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    path = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    summary = Column(String(255), nullable=True)
    category = Column(String(255), nullable=True)
    document_metatag_collection = relationship('document_metatag', back_populates='document')
