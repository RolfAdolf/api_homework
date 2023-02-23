from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class TankRequest(BaseModel):
    name: str
    max_capacity: float
    current_capacity: float
    product_id: int
