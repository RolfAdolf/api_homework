from datetime import datetime
from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session
from src.db.db import get_session
from src.models.tank import Tank
from src.models.schemas.tank.tank_request import TankRequest


class TanksService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def all(self) -> List[Tank]:
        tanks = (
            self.session
            .query(Tank)
            .order_by(
                Tank.id.desc()
            )
            .all()
        )
        return tanks

    def get(self, tank_id: int) -> Tank:
        tank = (
            self.session
            .query(Tank)
            .filter(
                Tank.id == tank_id
            )
            .first()
        )
        return tank

    def add(self, tank_schema: TankRequest, created_user_id: int) -> Tank:
        datetime_ = datetime.utcnow()
        tank = Tank(
            **tank_schema.dict(),
            created_at=datetime_,
            created_by=created_user_id,
            modified_at=datetime_,
            modified_by=created_user_id
        )
        self.session.add(tank)
        self.session.commit()
        return tank

    def update(self, tank_id: int, tank_schema: TankRequest, modified_user_id: int) -> Tank:
        tank = self.get(tank_id)
        for field, value in tank_schema:
            setattr(tank, field, value)
        datetime_ = datetime.utcnow()
        setattr(tank, 'modified_at', datetime_)
        setattr(tank, 'modified_by', modified_user_id)
        self.session.commit()
        return tank

    def delete(self, tank_id: int):
        tank = self.get(tank_id)
        self.session.delete(tank)
        self.session.commit()
