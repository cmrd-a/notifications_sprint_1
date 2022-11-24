from pydantic import BaseSettings, Field, EmailStr


class Settings(BaseSettings):
    sender_email: EmailStr = Field(env="SENDER_EMAIL")
    sender_password: str = Field(env="SENDER_PASSWORD")

    rabbit_host: str = Field(env="RABBIT_HOST", default="localhost")


settings = Settings()
