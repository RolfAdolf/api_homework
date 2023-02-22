from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session
from src.db.db import get_session
from src.models.user import User
from src.models.schemas.user.user_request import UserRequest


class UsersService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def all(self) -> List[User]:
        users = (
            self.session
            .query(User)
            .order_by(
                User.id.desc()
            )
            .all()
        )
        return users

    def get(self, user_id: int) -> User:
        user = (
            self.session
            .query(User)
            .filter(
                User.id == user_id
            )
            .first()
        )
        return user

    def add(self, user_schema: UserRequest) -> User:
        user = User(**user_schema.dict())
        self.session.add(user)
        self.session.commit()
        return user

    def update(self, user_id: int, user_schema: UserRequest) -> User:
        user = self.get(user_id)
        for field, value in user_schema:
            setattr(user, field, value)
        self.session.commit()
        return user

    def delete(self, user_id: int):
        user = self.get(user_id)
        self.session.delete(user)
        self.session.commit()
