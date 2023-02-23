from datetime import datetime

from src.models.user import User
from src.db.db import Session
from src.core.settings import settings
from src.services.users import UsersService

admin = User(
    username=settings.admin_login,
    password_hash=UsersService.hash_password(settings.admin_password),
    role='admin',
    created_at=datetime.utcnow(),
    created_by=None,
    modified_at=datetime.utcnow(),
    modified_by=None
)


def create_admin():
    session = Session()
    previous_admin = (
        session
        .query(User)
        .filter(
            User.username == settings.admin_login
        )
        .first()
    )
    if previous_admin:
        if UsersService.check_password(settings.admin_password, previous_admin.password_hash):
            session.close()
        else:
            session.delete(previous_admin)
            session.add(admin)
            session.commit()
            session.close()
    else:
        session.add(admin)
        session.commit()
        session.close()
