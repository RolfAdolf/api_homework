from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session
from src.db.db import get_session
from src.models.product import Product
from src.models.schemas.product.product_request import ProductRequest


class ProductsService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def all(self) -> List[Product]:
        products = (
            self.session
            .query(Product)
            .order_by(
                Product.id.desc()
            )
            .all()
        )
        return products

    def get(self, product_id: int) -> Product:
        product = (
            self.session
            .query(Product)
            .filter(
                Product.id == product_id
            )
            .first()
        )
        return product

    def add(self, product_schema: ProductRequest) -> Product:
        product = Product(**product_schema.dict())
        self.session.add(product)
        self.session.commit()
        return product

    def update(self, product_id: int, product_schema: ProductRequest) -> Product:
        product = self.get(product_id)
        for field, value in product_schema:
            setattr(product, field, value)
        self.session.commit()
        return product

    def delete(self, product_id: int):
        product = self.get(product_id)
        self.session.delete(product)
        self.session.commit()
