import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse

from src.models.schemas.operation.operation_request import OperationRequest
from src.models.schemas.operation.operation_response import OperationResponse, OperationResponseAll
from src.services.operations import OperationsService
from src.services.users import get_current_user_id
from src.models.schemas.file.file_request import FileRequest
from src.services.tanks import TanksService
from src.services.products import ProductsService


router = APIRouter(
    prefix='/operations',
    tags=['operations']
)


@router.get('/all', response_model=List[OperationResponseAll], name="Получить все")
def get(
        operation_service: OperationsService = Depends(),
        called_user_id: int = Depends(get_current_user_id),
        tank_service: TanksService = Depends(),
        product_service: ProductsService = Depends()
        ):
    """
    Получить все операции.
    Вложенные объекты tank и product.
    """
    operations = operation_service.all()
    for operation in operations:
        operation.tank = tank_service.get(operation.tank_id)
        operation.product = product_service.get(operation.product_id)
    return operations


@router.get('/get/{operation_id}', response_model=OperationResponse, name="Получить одну")
def get(
        operation_id: int,
        operations_service: OperationsService = Depends(),
        called_user_id: int = Depends(get_current_user_id)
        ):
    """
    Получить одну операцию по id.
    """
    return get_with_check(operation_id, operations_service)


def get_with_check(operation_id: int, operations_service: OperationsService):
    result = operations_service.get(operation_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Операция не найдена")
    return result


@router.post('/', response_model=OperationResponse, status_code=status.HTTP_201_CREATED, name="Добавить")
def add(
        operation_schema: OperationRequest,
        operations_service: OperationsService = Depends(),
        called_user_id: int = Depends(get_current_user_id)
        ):
    """
    Добавить одну операцию.
    """
    return operations_service.add(operation_schema, called_user_id)


@router.put('/{operation_id}', response_model=OperationResponse, name="Обновить информацию")
def put(
        operation_id: int,
        operation_schema: OperationRequest,
        operations_service: OperationsService = Depends(),
        called_user_id: int = Depends(get_current_user_id)
        ):
    """
    Обновить информацию об операции.
    """
    get_with_check(operation_id, operations_service)
    return operations_service.update(operation_id, operation_schema, called_user_id)


@router.delete('/{operation_id}', status_code=status.HTTP_204_NO_CONTENT, name="Удалить")
def delete(
        operation_id: int,
        operations_service: OperationsService = Depends(),
        called_user_id: int = Depends(get_current_user_id)
):
    """
    Удалить одну операцию по id.
    """
    get_with_check(operation_id, operations_service)
    return operations_service.delete(operation_id)


@router.get('/download', name='Скачать')
def download(
        tank_id: int,
        product_id: int,
        date_start: datetime.datetime,
        date_end: datetime.datetime,
        operation_service: OperationsService = Depends(),
        called_user_id: int = Depends(get_current_user_id)
        ):
    """
    Скачать операции, удовлетворяющие ограничениям, csv файлом.
    """
    file_schema = FileRequest(
        tank_id=tank_id,
        product_id=product_id,
        date_start=date_start,
        date_end=date_end
    )
    report = operation_service.download_operations(file_schema)
    return StreamingResponse(report, media_type='text/csv',
                             headers={'Content-Disposition': 'attachment; filename=report.csv'})


@router.get('/all_for_tank', response_model=List[OperationResponse], name="Получить для одного резервуара")
def get_for_tank(
        tank_id: int,
        operations_service: OperationsService = Depends(),
        called_user_id: int = Depends(get_current_user_id),
        tank_service: TanksService = Depends()
        ):
    """
    Получить операции над конкретным резервуаром.
    """
    result = tank_service.get(tank_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Резервуар не найден")
    return operations_service.get_for_tank(tank_id)
