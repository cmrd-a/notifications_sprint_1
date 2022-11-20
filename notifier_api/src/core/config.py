import os
from logging import config as logging_config

from pydantic import BaseSettings, Field

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    project_name: str = Field(env="PROJECT_NAME", default="notifier")
    pg_db_name: str = Field(env="POSTGRES_DB")
    pg_db_user: str = Field(env="POSTGRES_USER")
    pg_db_password: str = Field(env="POSTGRES_PASSWORD")
    pg_db_host: str = Field(env="POSTGRES_DB_HOST")
    pg_db_port: str = Field(env="POSTGRES_DB_PORT")

    @property
    def pg_connection_params(self):
        return {
            "dbname": self.pg_db_name,
            "user": self.pg_db_user,
            "password": self.pg_db_password,
            "host": self.pg_db_host,
            "port": self.pg_db_port,
        }


config = Settings()
