from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    JSONBIN_API_KEY: str
    JSONBIN_BIN_ID: str
    JSONBIN_API_URL: str = "https://api.jsonbin.io/v3"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def get_settings() -> Settings:
    return Settings() 