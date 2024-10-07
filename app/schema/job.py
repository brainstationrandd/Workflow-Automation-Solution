from pydantic import BaseModel
from datetime import datetime
from typing import Optional as optional
from typing import Any


class JobBase(BaseModel):
    user_id: int
    name: str
    description: optional[str] = None
    end_time: datetime


class JobUpdate(BaseModel):
    name: optional[str] = None
    description: optional[str] = None
    user_id: optional[int] = None

class JobResponseBase(JobBase):
    status_code: int
    message: str
    data: Any