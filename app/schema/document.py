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

class UpdateDocument(BaseModel):
    path: optional[str] = None
    summary: optional[str] = None
    category: optional[str] = None

class DocumentResponseBase(UpdateDocument):
    id: int
    created_at: datetime
    updated_at: datetime    

class DocumentResponse(BaseModel):
    status_code: int
    message: str
    data: DocumentResponseBase