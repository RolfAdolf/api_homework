from fastapi import FastAPI

from src.api.base_router import router


app = FastAPI(
    title='Домашнее задание',
    description='Домашнее задание по спринту #6.',
    version='0.0.1',
)

app.include_router(router)
