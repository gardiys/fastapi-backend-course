from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    jsonbin_api_key: str
    jsonbin_bin_id: str
    cloudflare_api_key: str
    cloudflare_account_id: str

    class Config:
        env_file = ".env"


settings = Settings()
