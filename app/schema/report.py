from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional as optional
from typing import List


class ReportBase(BaseModel):
    