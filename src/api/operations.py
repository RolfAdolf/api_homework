import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse

from src.models.schemas.operation.operation_request import OperationRequest
from src.models.schemas.operation.operation_response import OperationResponse
from src.services.operations import OperationsService
from src.services.users import get_current_user_id
from src.models.schemas.file.file_request import FileRequest


router = APIRouter(
    prefix='/operations',
    tags=['operations']
)


@router.get('/all', response_model=List[OperationResponse], name="Получить все операция")
def get(operation_service: OperationsService = Depends(), called_user_id: int = Depends(get_current_user_id)):
    """
    Получить все резервуары. Более подробное описание.
    """
    return operation_service.all()


@router.get('/get/{operation_id}', response_model=OperationResponse, name="Получить одну операцию")
def get(
        operation_id: int,
        operations_service: OperationsService = Depends(),
        called_user_id: int = Depends(get_current_user_id)
        ):
    return get_with_check(operation_id, operations_service)


def get_with_check(operation_id: int, operations_service: OperationsService):
    result = operations_service.get(operation_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Категория не найдена")
    return result


@router.post('/', response_model=OperationResponse, status_code=status.HTTP_201_CREATED, name="Добавить категорию")
def add(
        operation_schema: OperationRequest,
        operations_service: OperationsService = Depends(),
        called_user_id: int = Depends(get_current_user_id)
        ):
    return operations_service.add(operation_schema, called_user_id)


@router.put('/{operation_id}', response_model=OperationResponse, name="Обновить информацию о категории")
def put(
        operation_id: int,
        operation_schema: OperationRequest,
        operations_service: OperationsService = Depends(),
        called_user_id: int = Depends(get_current_user_id)
        ):
    get_with_check(operation_id, operations_service)
    return operations_service.update(operation_id, operation_schema, called_user_id)


@router.delete('/{operation_id}', status_code=status.HTTP_204_NO_CONTENT, name="Удалить категорию")
def delete(operation_id: int, operations_service: OperationsService = Depends()):
    get_with_check(operation_id, operations_service)
    return operations_service.delete(operation_id)


@router.get('/download', name='Скачивание файла')
def download(
        tank_id: int,
        product_id: int,
        date_start: datetime.datetime,
        date_end: datetime.datetime,
        operation_service: OperationsService = Depends()
        ):
    file_schema = FileRequest(
        tank_id=tank_id,
        product_id=product_id,
        date_start=date_start,
        date_end=date_end
    )
    report = operation_service.download_operations(file_schema)
    return StreamingResponse(report, media_type='text/csv',
                             headers={'Content-Disposition': 'attachment; filename=report.csv'})
