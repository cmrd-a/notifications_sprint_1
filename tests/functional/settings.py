from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    es_host: str = Field(env="ES_HOST", default="http://localhost")
    es_port: str = Field(env="ES_PORT", default=9200)

    redis_host: str = Field(env="REDIS_HOST", default="redis://localhost")
    redis_port: int = Field(env="REDIS_PORT", default=6379)

    fastapi_host: str = Field(env="FASTAPI_HOST", default="http://localhost")
    fastapi_port: int = Field(env="FASTAPI_PORT", default=5000)

    flask_host: str = Field(env="FLASK_HOST", default="http://localhost")
    flask_port: int = Field(env="FLASK_PORT", default=9000)

    @property
    def es_url(self):
        return f"{self.es_host}:{self.es_port}"

    @property
    def redis_url(self):
        return f"{self.redis_host}:{self.redis_port}"

    @property
    def fastapi_url(self):
        return f"{self.fastapi_host}:{self.fastapi_port}"

    @property
    def flask_url(self):
        return f"{self.flask_host}:{self.flask_port}/auth"


settings = Settings()
