from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from src.models.schemas.tank.tank_request import TankRequest
from src.models.schemas.tank.tank_response import TankResponse
from src.services.tanks import TanksService


router = APIRouter(
    prefix='/tanks',
    tags=['tanks']
)


@router.get('/all', response_model=List[TankResponse], name="Получить все резервуары")
def get(tank_service: TanksService = Depends()):
    """
    Получить все резервуары. Более подробное описание.
    """
    return tank_service.all()


@router.get('/get/{tank_id}', response_model=TankResponse, name="Получить одну категорию")
def get(tank_id: int, tanks_service: TanksService = Depends()):
    return get_with_check(tank_id, tanks_service)


def get_with_check(tank_id: int, tanks_service: TanksService):
    result = tanks_service.get(tank_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Категория не найдена")
    return result


@router.post('/', response_model=TankResponse, status_code=status.HTTP_201_CREATED, name="Добавить категорию")
def add(tank_schema: TankRequest, tanks_service: TanksService = Depends()):
    return tanks_service.add(tank_schema)


@router.put('/{tank_id}', response_model=TankResponse, name="Обновить информацию о категории")
def put(tank_id: int, tank_schema: TankRequest, tanks_service: TanksService = Depends()):
    get_with_check(tank_id, tanks_service)
    return tanks_service.update(tank_id, tank_schema)


@router.delete('/{tank_id}', status_code=status.HTTP_204_NO_CONTENT, name="Удалить категорию")
def delete(tank_id: int, tanks_service: TanksService = Depends()):
    get_with_check(tank_id, tanks_service)
    return tanks_service.delete(tank_id)
