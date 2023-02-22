from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session
from src.db.db import get_session
from src.models.operation import Operation
from src.models.schemas.operation.operation_request import OperationRequest


class OperationsService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def all(self) -> List[Operation]:
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

    def add(self, operation_schema: OperationRequest) -> Operation:
        operation = Operation(**operation_schema.dict())
        self.session.add(operation)
        self.session.commit()
        return operation

    def update(self, operation_id: int, operation_schema: OperationRequest) -> Operation:
        operation = self.get(operation_id)
        for field, value in operation_schema:
            setattr(operation, field, value)
        self.session.commit()
        return operation

    def delete(self, operation_id: int):
        operation = self.get(operation_id)
        self.session.delete(operation)
        self.session.commit()
