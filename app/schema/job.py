# from pydantic import BaseModel
# from datetime import datetime
# from typing import Optional as optional
# from typing import Any


# class JobBase(BaseModel):
#     user_id: int
#     name: str
#     description: optional[str] = None
#     end_time: datetime


# class JobUpdate(BaseModel):
#     name: optional[str] = None
#     description: optional[str] = None
#     user_id: optional[int] = None

# class JobResponseBase(JobBase):
#     status_code: int
#     message: str
#     data: Any

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional as optional, Any
from enum import Enum


# Define the JobStatus Enum to match the SQLAlchemy model's enum
class JobStatus(str, Enum):
    active = "active"
    archived = "archived"


class JobBase(BaseModel):
    user_id: int
    name: str
    description: optional[str] = None
    end_time: optional[datetime] = None
    status: JobStatus = JobStatus.active  # Default status as "active"

class JobUpdate(BaseModel):
    name: optional[str] = None
    description: optional[str] = None
    status: optional[JobStatus] = None  # Allow updating status
    end_time: optional[datetime] = None
class JobResponseBase(BaseModel):
    status_code: int
    message: str
    data: Any


# Example response model for returning job details
class JobResponse(JobResponseBase):
    data: JobBase
