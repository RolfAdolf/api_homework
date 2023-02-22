from pydantic import BaseModel
from datetime import datetime


class ProductResponse(BaseModel):
    id: int
    name: str
    created_at: datetime
    created_by: int
    modified_at: datetime
    modified_by: int
