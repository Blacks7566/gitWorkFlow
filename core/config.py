from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import Set


class Settings(BaseSettings):
    PROJECT_NAME: str = "Image Api"
    AWS_CLIENT_ACCESS_KEY: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_BUCKET: str
    AWS_REGIN: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
