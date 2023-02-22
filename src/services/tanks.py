from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session
from src.db.db import get_session
from src.models.tank import Tank
from src.models.schemas.tank.tank_request import TankRequest


class TanksService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = Session

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

    def add(self, tank_schema: TankRequest) -> Tank:
        tank = Tank(**tank_schema.dict())
        self.session.add(tank)
        self.session.commit()
        return tank

    def update(self, tank_id: int, tank_schema: TankRequest) -> Tank:
        tank = self.get(tank_id)
        for field, value in tank_schema:
            setattr(tank, field, value)
        self.session.commit()
        return tank

    def delete(self, tank_id: int):
        tank = self.get(tank_id)
        self.session.delete(tank)
        self.session.commit()
