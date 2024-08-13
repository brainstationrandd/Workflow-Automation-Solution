from sqlalchemy import Column, Integer, String, DateTime, Boolean, func, ForeignKey, Enum
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
    classification_status = Column(Enum('NOT STARTED', 'IN PROGRESS', 'DONE', 'COMPLETED', 'FAILED', name='status'), default='NOT STARTED', nullable=True)
    document_metatag = relationship('Document_metatag', back_populates='document')


from app.models.document_metatag import Document_metatag