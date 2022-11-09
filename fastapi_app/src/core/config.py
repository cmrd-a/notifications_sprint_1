import os
from logging import config as logging_config

from pydantic import BaseSettings, Field

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    project_name: str = Field(env="PROJECT_NAME", default="movies")

    es_host: str = Field(env="ES_API_HOST", default="http://127.0.0.1")
    es_port: int = Field(env="ES_API_PORT", default=9200)

    redis_host: str = Field(env="REDIS_HOST", default="redis://127.0.0.1")
    redis_port: int = Field(env="REDIS_PORT", default=6379)
    redis_cache_expire_in_seconds: int = Field(env="REDIS_CACHE_EXPIRE_IN_SECONDS", default=300)

    auth_host: str = Field(env="AUTH_HOST", default="http://localhost")
    auth_port: int = Field(env="AUTH_PORT", default=9000)

    kafka_server: str = Field(env="KAFKA_SERVER", default="localhost:9092")

    sentry_dsn: str = Field(env="SENTRY_FASTAPI_DSN")
    sentry_enabled: bool = Field(env="SENTRY_ENABLED", default=False)

    @property
    def es_url(self):
        return f"{self.es_host}:{self.es_port}"

    @property
    def redis_url(self):
        return f"{self.redis_host}:{self.redis_port}"

    @property
    def auth_url(self):
        return f"{self.auth_host}:{self.auth_port}"


config = Settings()
