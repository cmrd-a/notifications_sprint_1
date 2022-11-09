from logging import config as logging_config

from pydantic import BaseSettings, Field

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    project_name: str = Field(default="User generated content")
    mongo_host: str = Field(env="MONGO_UGC_HOST", default="localhost")
    mongo_port: int = Field(env="MONGO_UGC_PORT", default=27017)
    mongo_user: str = Field(env="MONGO_INITDB_ROOT_USERNAME", default="root")
    mongo_password: str = Field(env="MONGO_INITDB_ROOT_PASSWORD", default="example")

    @property
    def mongo_url(self):
        return f"mongodb://{self.mongo_user}:{self.mongo_password}@{self.mongo_host}:{self.mongo_port}"


config = Settings()
