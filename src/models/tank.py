from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from src.models.base import Base
from sqlalchemy.orm import relationship
from src.models.product import Product
from src.models.user import User

class Tank(Base):

    __tablename__ = 'tanks'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    max_capacity = Column(Float)
    current_capacity = Column(Float)
    product_id = Column(Integer, ForeignKey('products.id'))
    created_at = Column(DateTime)
    created_by = Column(Integer, ForeignKey('users.id'))
    modified_at = Column(DateTime)
    modified_by = Column(Integer, ForeignKey('users.id'))

    product = relationship('Product', backref='tanks')
    user_create = relationship('User', foreign_keys=[created_by], backref='created_tanks')
    user_modified = relationship('User', foreign_keys=[modified_by], backref='modified_tanks')