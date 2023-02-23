from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class OperationResponse(BaseModel):
    id: int
    mass: float
    date_start: datetime
    date_end: datetime
    tank_id: Optional[int]
    product_id: Optional[int]
    created_at: datetime
    created_by: Optional[int]
    modified_at: datetime
    modified_by: Optional[int]

    class Config:
        orm_mode = True
