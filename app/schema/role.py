from pydantic import BaseModel
from datetime import datetime
from typing import Optional as optional
from typing import List

class RoleBase(BaseModel):
    name: str

class RoleUpdate(BaseModel):
    name: optional[str] = None


