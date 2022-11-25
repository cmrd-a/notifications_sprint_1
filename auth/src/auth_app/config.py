from datetime import timedelta

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    APPLICATION_ROOT = "/auth"
    DEBUG: bool = Field(env="FLASK_DEBUG", default=False)
    SECRET_KEY: str = Field(env="SECRET_KEY")

    pg_db_name: str = Field(env="POSTGRES_DB")
    pg_db_user: str = Field(env="POSTGRES_USER")
    pg_db_password: str = Field(env="POSTGRES_PASSWORD")
    pg_db_host: str = Field(env="POSTGRES_DB_HOST")
    pg_db_port: str = Field(env="POSTGRES_DB_PORT")
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    REDIS_HOST: str = Field(env="REDIS_HOST", default="redis://redis")
    REDIS_PORT: str = Field(env="REDIS_PORT", default=6379)
    JWT_SECRET_KEY: str = Field(env="SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    SPEC_FORMAT: str = Field(env="SPEC_FORMAT", default="yaml")
    ENABLE_TRACING: bool = Field(env="ENABLE_TRACING", default=False)
    jaeger_host: str = Field(env="JAEGER_HOST", default="localhost")
    jaeger_port: int = Field(env="JAEGER_PORT", default=6831)
    RATELIMIT_DEFAULT: str = Field(env="RATELIMIT_DEFAULT", default="10 per second")
    GOOGLE_CLIENT_ID: str = Field(env="GOOGLE_CLIENT_ID", default="")
    GOOGLE_CLIENT_SECRET: str = Field(env="GOOGLE_CLIENT_SECRET", default="")
    GOOGLE_DISCOVERY_URL: str = Field(default="https://accounts.google.com/.well-known/openid-configuration")
    sentry_enabled: bool = Field(env="SENTRY_ENABLED", default=False)
    sentry_dsn: str = Field(env="SENTRY_FLASK_DSN")
    logstash_host: str = Field(env="LOGSTASH_HOST")
    logstash_port: int = Field(env="LOGSTASH_PORT")

    notificator_url: str = Field(env="NOTIFICATOR_URL", default="http://localhost")
    confirm_host: str = Field(env="CONFIRM_HOST", default="http://localhost")

    @property
    def SQLALCHEMY_DATABASE_URI(self):  # noqa
        return (
            f"postgresql+psycopg2://{self.pg_db_user}:{self.pg_db_password}"
            f"@{self.pg_db_host}:{self.pg_db_port}/{self.pg_db_name}"
        )

    @property
    def REDIS_URL(self):  # noqa
        return f"{self.REDIS_HOST}:{self.REDIS_PORT}"

    @property
    def RATELIMIT_STORAGE_URI(self):  # noqa
        return self.REDIS_URL


config = Settings()
