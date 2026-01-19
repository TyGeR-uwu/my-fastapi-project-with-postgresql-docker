from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    db_user: str = Field(default="postgres", env="DB_USER")
    db_pass: str = Field(default="", env="DB_PASSWORD")
    db_host: str = Field(default="db", env="DB_HOST")
    db_port: str = Field(default="5432", env="DB_PORT")
    db_name: str = Field(default="postgres", env="DB_NAME")

    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")

    class Config:
        env_file = ".env"


settings = Settings()