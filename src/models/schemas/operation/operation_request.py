from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class OperationRequest(BaseModel):
    mass: float
    date_start: datetime
    date_end: datetime
    tank_id: int
    product_id: int
    created_at: datetime
    created_by: int
    modified_at: datetime
    modified_by: int
