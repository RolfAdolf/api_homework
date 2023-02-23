from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class UserResponse(BaseModel):
    id: int
    username: str
    password_hash: str
    role: str
    created_at: datetime
    created_by: Optional[int]
    modified_at: datetime
    modified_by: Optional[int]

    class Config:
        orm_mode = True
