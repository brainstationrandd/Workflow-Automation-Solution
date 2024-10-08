from sqlalchemy import Column, Integer, String, DateTime, Boolean, func, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.db import Base

metadata = Base.metadata

class Document(Base):
    __tablename__ = 'document'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    job_id = Column(Integer, ForeignKey('job.id'), nullable=False)
    path = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    summary = Column(String(255), nullable=True)
    comprehend_job_id = Column(String(255), nullable=True)
    category = Column(String(255), nullable=True)
    sub_category = Column(String(255), nullable=True)
    classification_status = Column(Enum('NOT STARTED', 'IN PROGRESS', 'DONE', 'COMPLETED', 'FAILED', name='status'), default='NOT STARTED', nullable=True)
    pdf_hash = Column(String(64), nullable=False)  # New column to store the hash
    document_metatag = relationship('Document_metatag', back_populates='document')


from app.models.document_metatag import Document_metatag
from app.models.job import Job