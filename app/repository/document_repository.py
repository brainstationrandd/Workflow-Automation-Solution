from fastapi import HTTPException
from requests import Session
from utils.logger import logger
from app.db import engine, SessionLocal, Base, get_db
from app.models.document import Document


class DocumentRepository:
    @staticmethod
    async def get_doc_by_id(document_id):
        db = SessionLocal()
        try:
            user = db.query(Document).filter(Document.id == document_id).first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return user
        except HTTPException as e:
            logger.info(f'An HTTP error occurred: \n {str(e)}')
            raise e
        except Exception as e:
            logger.info(f'An error occurred: \n {str(e)}')
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
        
    
