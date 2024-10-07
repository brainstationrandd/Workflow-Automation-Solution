from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional as optional
from typing import List

class UserBase(BaseModel):
    name: str
    email: str
    password: str
    password: optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str

class UpdateUser(BaseModel):
    name: optional[str] = None
    email: optional[str] = None
    avatar: optional[str] = None
    password: optional[str] = None
    

class UpdateUserPassword(BaseModel):
    password: str
    new_password: str
    confirm_password: str

class UserCreate(UserBase):
    password: str


class UserResponseBase(UpdateUser):
    id: int
    created_at: datetime
    updated_at: datetime

class UserResponse(BaseModel):
    status_code: int
    message: str
    data: UserResponseBase
    

class UserResponseWithMessage(BaseModel):
    message: str
    data: List[UserResponseBase]
    total: int


class User(UserBase):
    id: int

    class Config:
        from_attributes = True