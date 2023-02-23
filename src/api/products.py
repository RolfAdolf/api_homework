from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from src.models.schemas.product.product_request import ProductRequest
from src.models.schemas.product.product_response import ProductResponse
from src.services.products import ProductsService
from src.services.users import get_current_user_id


router = APIRouter(
    prefix='/products',
    tags=['products']
)


@router.get('/all', response_model=List[ProductResponse], name="Получить все резервуары")
def get(product_service: ProductsService = Depends(), user_id: int = Depends(get_current_user_id)):
    """
    Получить все продукты. Более подробное описание.
    """
    return product_service.all()


@router.get('/get/{product_id}', response_model=ProductResponse, name="Получить одну категорию")
def get(product_id: int, products_service: ProductsService = Depends(), user_id: int = Depends(get_current_user_id)):
    return get_with_check(product_id, products_service)


def get_with_check(product_id: int, products_service: ProductsService):
    result = products_service.get(product_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Категория не найдена")
    return result


@router.post('/', response_model=ProductResponse, status_code=status.HTTP_201_CREATED, name="Добавить категорию")
def add(
        product_schema: ProductRequest,
        products_service: ProductsService = Depends(),
        called_user_id: int = Depends(get_current_user_id)
        ):
    return products_service.add(product_schema, called_user_id)


@router.put('/{product_id}', response_model=ProductResponse, name="Обновить информацию о категории")
def put(
        product_id: int,
        product_schema: ProductRequest,
        products_service: ProductsService = Depends(),
        called_user_id: int = Depends(get_current_user_id)
        ):
    get_with_check(product_id, products_service)
    return products_service.update(product_id, product_schema, called_user_id)


@router.delete('/{product_id}', status_code=status.HTTP_204_NO_CONTENT, name="Удалить категорию")
def delete(product_id: int, products_service: ProductsService = Depends()):
    get_with_check(product_id, products_service)
    return products_service.delete(product_id)
