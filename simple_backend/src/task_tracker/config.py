from pydantic_settings import BaseSettings
from starlette.config import Config

config = Config(".env")

class Settings(BaseSettings):
    BIN_ID: str = config("BIN_ID", cast=str)
    MASTER_KEY: str = config("MASTER_KEY", cast=str)
    API_TOKEN_AI: str = config("API_TOKEN_AI", cast=str)
    ACCOUNT_ID_AI: str = config("ACCOUNT_ID_AI", cast=str)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
