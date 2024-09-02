from fastapi import HTTPException
from requests import Session
from utils.logger import logger
from app.db import engine, SessionLocal, Base, get_db
from app.models.document import Document
from app.schema.document import *


class DocumentRepository:
    @staticmethod
    def get_doc_by_id(document_id: int):
        db = SessionLocal()
        try:
            doc = db.query(Document).filter(Document.id == document_id).first()
            if not doc:
                raise HTTPException(status_code=404, detail="Document not found")
            return doc
        except HTTPException as e:
            logger.info(f'An HTTP error occurred: \n {str(e)}')
            raise e
        except Exception as e:
            logger.info(f'An error occurred: \n {str(e)}')
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
        
    @staticmethod
    def get_doc_by_comprehend_job_id(job_id: int):
        db = SessionLocal()
        try:
            doc = db.query(Document).filter(Document.comprehend_job_id == job_id).first()
            if not doc:
                raise HTTPException(status_code=404, detail="Document not found")
            return doc
        except HTTPException as e:
            logger.info(f'An HTTP error occurred: \n {str(e)}')
            raise e
        except Exception as e:
            logger.info(f'An error occurred: \n {str(e)}')
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
        
    @staticmethod
    def update_doc_by_comprehend_job_id(job_id: int, document: UpdateDocumentComprehend):
        db = SessionLocal()
        # logger.info(f"entering db for {job_id}")
        try:
            doc = db.query(Document).filter(Document.comprehend_job_id == job_id).first()
            if not doc:
                raise HTTPException(status_code=404, detail="Document not found")
            if document.classification_status:
                doc.classification_status = document.classification_status
            if document.category:
                doc.category = document.category
                logger.info(f"db (category) updated for {job_id}")
            if document.sub_category:
                doc.sub_category = document.sub_category
                logger.info(f"db (subcategory) updated for {job_id}")

            db.commit()
            db.refresh(doc)
            return doc
        except HTTPException as e:
            logger.info(f'An HTTP error occurred: \n {str(e)}')
            raise e
        except Exception as e:
            logger.info(f'An error occurred: \n {str(e)}')
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

    @staticmethod
    def update_doc_status(document_id: int,document: UpdateDocument):
        db = SessionLocal()
        try:
            doc = db.query(Document).filter(Document.id == document_id).first()
            if doc:
                if document.classification_status:
                    doc.classification_status = document.classification_status
                if document.category:
                    doc.category = document.category
                if document.sub_category:
                    doc.sub_category = document.sub_category
                if document.path:
                    doc.path = document.path
                if document.comprehend_job_id:
                    doc.comprehend_job_id = document.comprehend_job_id
                db.commit()
                db.refresh(doc)
            return doc
        except HTTPException as e:
            logger.info(f'An HTTP error occurred: \n {str(e)}')
            raise e
        except Exception as e:
            logger.info(f'An error occurred: \n {str(e)}')
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
        
    @staticmethod
    def add_file(document: DocumentBase):
        db = SessionLocal()
        try:
            db_file = Document(
                path = document.path,
                created_at = document.created_at,
                updated_at = document.updated_at,
                summary = document.summary,
                category = document.category,
                sub_category = document.sub_category,
                classification_status = document.classification_status,
                comprehend_job_id = document.comprehend_job_id,
                job_id = document.job_id
            )
            db.add(db_file)
            db.commit()
            db.refresh(db_file)
            return db_file
        except HTTPException as e:
            logger.info(f'An HTTP error occurred: \n {str(e)}')
            raise e
        except Exception as e:
            logger.info(f'An error occurred: \n {str(e)}')
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
