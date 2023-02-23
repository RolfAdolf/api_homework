from typing import List
from fastapi import Depends
from sqlalchemy import DateTime
from sqlalchemy.orm import Session
from datetime import datetime
import csv
from io import StringIO

from src.db.db import get_session
from src.models.operation import Operation
from src.models.schemas.operation.operation_request import OperationRequest
from src.models.schemas.file.file_request import FileRequest
from src.models.tank import Tank
from src.models.product import Product


class OperationsService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def all(self):
        operations = (
            self.session
            .query(Operation)
            .order_by(
                Operation.id.desc()
            )
            .all()
        )
        return operations

    def get(self, operation_id: int) -> Operation:
        operation = (
            self.session
            .query(Operation)
            .filter(
                Operation.id == operation_id
            )
            .first()
        )
        return operation

    def add(self, operation_schema: OperationRequest, created_user_id: int) -> Operation:
        datetime_ = datetime.utcnow()
        operation = Operation(
            **operation_schema.dict(),
            created_at=datetime_,
            created_by=created_user_id,
            modified_at=datetime_,
            modified_by=created_user_id
        )
        self.session.add(operation)
        self.session.commit()
        return operation

    def update(self, operation_id: int, operation_schema: OperationRequest, modified_user_id: int) -> Operation:
        operation = self.get(operation_id)
        for field, value in operation_schema:
            setattr(operation, field, value)
        datetime_ = datetime.utcnow()
        setattr(operation, 'modified_at', datetime_)
        setattr(operation, 'modiifed_by', modified_user_id)
        self.session.commit()
        return operation

    def delete(self, operation_id: int):
        operation = self.get(operation_id)
        self.session.delete(operation)
        self.session.commit()

    def download_operations(self, file_schema: FileRequest) -> StringIO:
        operations = (
            self.session
            .query(Operation)
            .filter(
                Operation.tank_id == file_schema.tank_id,
                Operation.product_id == file_schema.product_id,
                Operation.date_start < file_schema.date_start,
                Operation.date_end > file_schema.date_end
            )
            .all()
        )
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=["tank_id", "product_id", "date_start", "date_end"])
        writer.writeheader()
        for operation in operations:
            print(operation)
            writer.writerow(
                {
                    'tank_id': operation.tank_id,
                    'product_id': operation.product_id,
                    'date_start': operation.date_start,
                    'date_end': operation.date_end
                }
            )
        output.seek(0)
        return output

    def get_for_tank(self, tank_id: int):
        operations = (
            self.session
            .query(Operation)
            .filter(
                Operation.tank_id == tank_id
            )
            .all()
        )
        return operations
