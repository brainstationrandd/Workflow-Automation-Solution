from http.client import HTTPException
from fastapi import HTTPException as FastAPIHTTPException
from sqlalchemy.orm import Session
from app.repository.document_repository import DocumentRepository
from app.schema.user import UserBase
from utils.logger import logger
import os

def get_doc_by_id_service(id: int):
    try:
        doc = DocumentRepository.get_doc_by_id(id)
        return doc
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e