from typing import Optional, Literal
from pydantic import BaseModel
from datetime import datetime


class UserRequest(BaseModel):
    username: str
    password_text: str
    role: Literal['admin', 'viewer']