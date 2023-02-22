from pydantic import BaseSettings


class Settings(BaseSettings):
    host: str = 'localhost'
    port: int = 9999
    connection_string: str


settings = Settings(
    _env_file='~/api_homework/.env',
    _env_file_encoding='utf-8',
)
