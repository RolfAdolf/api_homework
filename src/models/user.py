from sqlalchemy import Column, Integer, String, DateTime
from src.models.base import Base
from sqlalchemy.orm import relationship


class User(Base):

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password_hash = Column(String)
    role = Column(String)
    created_at = Column(DateTime)
    created_by = Column(Integer, nullable=True)
    modified_at = Column(DateTime)
    modified_by = Column(Integer, nullable=True)
