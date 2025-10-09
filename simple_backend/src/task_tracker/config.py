from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class Settings(BaseSettings):
    CLOUDFLARE_AUTH_TOKEN: str
    CLOUDFLARE_ACCOUNT_ID: str
    CLOUDFLARE_MODEL: str
    GITHUB_TOKEN: str
    GIST_ID: str

    class Config:
        env_file = BASE_DIR / ".env"
        env_file_encoding = "utf-8"

settings = Settings()
