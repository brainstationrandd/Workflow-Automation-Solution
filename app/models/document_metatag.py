from sqlalchemy import Column, Integer, String, DateTime, Boolean, func, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base

class document_metatag(Base):
    __tablename__ = 'document_metatag'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    document_id = Column(Integer, ForeignKey('document.id'), nullable=False)
    metatag_id = Column(Integer, ForeignKey('metatag.id'), nullable=False)
    document = relationship('document', back_populates='document_metatag_collection')
    metatag = relationship('metatag', back_populates='document_metatag_collection')
