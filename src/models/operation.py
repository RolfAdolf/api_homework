from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from src.models.base import Base
from sqlalchemy.orm import relationship
from src.models.product import Product
from src.models.user import User
from src.models.tank import Tank


class Operation(Base):

    __tablename__ = 'operations'
    id = Column(Integer, primary_key=True)
    mass = Column(Float)
    date_start = Column(DateTime)
    date_end = Column(DateTime)
    tank_id = Column(Integer, ForeignKey('tanks.id'), nullable=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=True)
    created_at = Column(DateTime)
    created_by = Column(Integer, ForeignKey('users.id'), nullable=True)
    modified_at = Column(DateTime)
    modified_by = Column(Integer, ForeignKey('users.id'), nullable=True)
