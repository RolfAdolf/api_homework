from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from src.models.schemas.user.user_request import UserRequest
from src.models.schemas.user.user_response import UserResponse
from src.services.users import UsersService


router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.get('/all', response_model=List[UserResponse], name="Получить все резервуары")
def get(user_service: UsersService = Depends()):
    """
    Получить все резервуары. Более подробное описание.
    """
    return user_service.all()


@router.get('/get/{user_id}', response_model=UserResponse, name="Получить одну категорию")
def get(user_id: int, users_service: UsersService = Depends()):
    return get_with_check(user_id, users_service)


def get_with_check(user_id: int, users_service: UsersService):
    result = users_service.get(user_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Категория не найдена")
    return result


@router.post('/', response_model=UserResponse, status_code=status.HTTP_201_CREATED, name="Добавить категорию")
def add(user_schema: UserRequest, users_service: UsersService = Depends()):
    return users_service.add(user_schema)


@router.put('/{user_id}', response_model=UserResponse, name="Обновить информацию о категории")
def put(user_id: int, user_schema: UserRequest, users_service: UsersService = Depends()):
    get_with_check(user_id, users_service)
    return users_service.update(user_id, user_schema)


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT, name="Удалить категорию")
def delete(user_id: int, users_service: UsersService = Depends()):
    get_with_check(user_id, users_service)
    return users_service.delete(user_id)
