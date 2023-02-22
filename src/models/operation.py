from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from src.models.base import Base
from sqlalchemy.orm import relationship


class Operation(Base):

    __tablename__ = 'operations'
    id = Column(Integer, primary_key=True)
    mass = Column(Float)
    date_start = Column(DateTime)
    date_end = Column(DateTime)
    tank_id = Column(Integer, ForeignKey('tanks'))
    product_id = Column(Integer, ForeignKey('products'))
    created_at = Column(DateTime)
    created_by = Column(int, ForeignKey('users'))
    modified_at = Column(DateTime)
    modified_by = Column(Integer, ForeignKey('users'))
