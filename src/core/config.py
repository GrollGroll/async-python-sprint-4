import os
from logging import config as logging_config

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)

class AppSettings(BaseSettings):
    app_title: str = "shortened_URL"
    database_dsn: PostgresDsn
    PROJECT_NAME: str = os.getenv('PROJECT_NAME', 'shortened_URL')
    PROJECT_HOST: str = os.getenv('PROJECT_HOST', '127.0.0.1')
    PROJECT_PORT: int = os.getenv('PROJECT_PORT', 8000)

    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    class Config:
        env_file = '.env'

app_settings = AppSettings()