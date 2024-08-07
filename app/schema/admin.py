from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from typing import List

class AdminBase(BaseModel):
    name: str
    email: str
    avatar: Optional[str] = None
    password: Optional[str] = None

class AdminCreate(AdminBase):
    password: str

class AdminResponseBase(AdminBase):
    id: int
    created_at: datetime
    updated_at: datetime

class AdminResponse(BaseModel):
    status_code: int
    message: str
    data: AdminResponseBase

class UpdateAdmin(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    avatar: Optional[str] = None
    # password: Optional[str] = None

class UpdateAdminPassword(BaseModel):
    password: str
    new_password: str
    confirm_password: str

class AllAdminResponse(BaseModel):
    message: str
    data: List[AdminResponseBase]
    total: int

class AdminResponseBase(UpdateAdmin):
    id: int
    created_at: datetime
    updated_at: datetime

class AdminResponse(BaseModel):
    status_code: int
    message: str
    data: AdminResponseBase

class Admin(AdminBase):
    id: int

    class Config:
        from_attributes = True