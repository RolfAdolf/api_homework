from pydantic import BaseModel
from datetime import datetime


class ProductRequest(BaseModel):
    name: str
