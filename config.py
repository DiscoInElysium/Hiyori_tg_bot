import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
    )
    bot_token: str
    admin_ids: int = os.getenv('admin_ids')


settings = Settings()
SQL_URL = os.getenv('SQL_URL')
