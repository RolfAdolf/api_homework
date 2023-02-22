from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class ProductRequest(BaseModel):
    name: str
    created_at: datetime
    created_by: int
    modified_at: datetime
    modified_by: int
