from fastapi import FastAPI

from src.api.base_router import router
from src.utils.create_admin import create_admin


app = FastAPI(
    title='Домашнее задание',
    description='Домашнее задание по спринту #6.',
    version='0.0.1',
)

create_admin()

app.include_router(router)
