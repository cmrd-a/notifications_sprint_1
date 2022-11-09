from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    kafka_server: str = Field(env="KAFKA_SERVER", default="localhost:9092")
    ch_server: str = Field(env="CLICKHOUSE_HOST", default="localhost")
    ch_user: str = Field(env="CLICKHOUSE_USER", default="admin")
    ch_password: str = Field(env="CLICKHOUSE_PASSWORD", default="123")


setting = Settings()
