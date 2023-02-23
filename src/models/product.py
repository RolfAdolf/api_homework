from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from src.models.base import Base
from sqlalchemy.orm import relationship


class Product(Base):

    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    created_at = Column(DateTime)
    created_by = Column(Integer, ForeignKey('users.id'), nullable=True)
    modified_at = Column(DateTime)
    modified_by = Column(Integer, ForeignKey('users.id'), nullable=True)

    user_create = relationship('User', foreign_keys=[created_by], backref='created_products')
    user_modified = relationship('User', foreign_keys=[modified_by], backref='modified_products')
