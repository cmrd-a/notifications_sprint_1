from pydantic import BaseSettings, Field, EmailStr


class Settings(BaseSettings):
    sender_email: EmailStr = Field(env="SENDER_EMAIL")
    sender_password: str = Field(env="SENDER_PASSWORD")
    smtp_host: str = Field(env="SMTP_HOST", default="smtp.yandex.ru")
    smtp_port: int = Field(env="SMTP_PORT", default=465)

    rabbit_host: str = Field(env="RABBIT_HOST", default="localhost")


settings = Settings()
