from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    pg_db_name: str = Field(env="NOTI_POSTGRES_DB")
    pg_db_user: str = Field(env="NOTI_POSTGRES_USER")
    pg_db_password: str = Field(env="NOTI_POSTGRES_PASSWORD")
    pg_db_host: str = Field(env="NOTI_POSTGRES_HOST")
    pg_db_port: str = Field(env="NOTI_POSTGRES_PORT")

    polling_frequency: float = Field(env="POLLING_FREQUENCY", default=2.0)

    rabbit_host: str = Field(env="RABBIT_HOST", default="localhost")

    @property
    def pg_connection_params(self):
        return {
            "dbname": self.pg_db_name,
            "user": self.pg_db_user,
            "password": self.pg_db_password,
            "host": self.pg_db_host,
            "port": self.pg_db_port,
        }


settings = Settings()
