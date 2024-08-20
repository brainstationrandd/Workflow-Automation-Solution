from pydantic import BaseModel
from datetime import datetime
from typing import Optional as optional
from typing import List


class JobBase(BaseModel):
    user_id: int
    name: str
    description: optional[str] = None