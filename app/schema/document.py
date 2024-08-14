from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional as optional
from typing import List


class DocumentBase(BaseModel):
    path: str
    created_at: datetime
    updated_at: datetime
    summary: str
    category: str
    sub_category: str
    classification_status: str = 'NOT STARTED'

class UpdateDocument(BaseModel):
    path: optional[str] = None
    summary: optional[str] = None
    category: optional[str] = None
    sub_category: optional[str] = None
    classification_status: optional[str] = None

class DocumentResponseBase(UpdateDocument):
    id: int
    created_at: datetime
    updated_at: datetime    

class DocumentResponse(BaseModel):
    status_code: int
    message: str
    data: DocumentResponseBase

class DocumentInit(BaseModel):
    path: str
    classification_status: str = 'NOT STARTED'

class DocumentWithMetadata(BaseModel):
    document_id: int
    bucket_name: str
    model_arn: str
    local_output_path: str
    document: DocumentBase
    job_id: str
