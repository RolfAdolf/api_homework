from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from src.models.schemas.tank.tank_request import TankRequest
from src.models.schemas.tank.tank_response import TankResponse
from src.services.tanks import TanksService
from src.services.users import get_current_user_id


router = APIRouter(
    prefix='/tanks',
    tags=['tanks']
)


@router.get('/all', response_model=List[TankResponse], name="Получить все")
def get(tank_service: TanksService = Depends(), user_id: int = Depends(get_current_user_id)):
    """
    Получить все резервуары.
    """
    return tank_service.all()


@router.get('/get/{tank_id}', response_model=TankResponse, name="Получить один")
def get(tank_id: int, tanks_service: TanksService = Depends(), user_id: int = Depends(get_current_user_id)):
    """
    Получить один резервуар по id.
    """
    return get_with_check(tank_id, tanks_service)


def get_with_check(tank_id: int, tanks_service: TanksService):
    result = tanks_service.get(tank_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Резервуар не найден")
    return result


@router.post('/', response_model=TankResponse, status_code=status.HTTP_201_CREATED, name="Добавить")
def add(tank_schema: TankRequest,
        tanks_service: TanksService = Depends(),
        called_user_id: int = Depends(get_current_user_id)
        ):
    """
    Добавить один резервуар.
    """
    return tanks_service.add(tank_schema, called_user_id)


@router.put('/{tank_id}', response_model=TankResponse, name="Обновить")
def put(tank_id: int, tank_schema: TankRequest,
        tanks_service: TanksService = Depends(),
        called_user_id: int = Depends(get_current_user_id)
        ):
    """
    Обновить информацию по конкретному резервуару.
    """
    get_with_check(tank_id, tanks_service)
    return tanks_service.update(tank_id, tank_schema, called_user_id)


@router.delete('/{tank_id}', status_code=status.HTTP_204_NO_CONTENT, name="Удалить")
def delete(
        tank_id: int,
        tanks_service: TanksService = Depends(),
        called_user_id: int = Depends(get_current_user_id)
        ):
    """
    Удалить один резервуар по id.
    """
    get_with_check(tank_id, tanks_service)
    return tanks_service.delete(tank_id)


@router.get('/{tank_id}', response_model=TankResponse, name="Поменять ёмкость")
def change_capacity(
        tank_id: int,
        current_capacity: float,
        tanks_service: TanksService = Depends(),
        called_user_id: int = Depends(get_current_user_id)
        ):
    """
    Поменять текущую ёмкость резервуара.
    """
    get_with_check(tank_id, tanks_service)
    return tanks_service.change_capacity(tank_id, current_capacity)
