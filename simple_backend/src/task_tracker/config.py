from pydantic_settings import BaseSettings, SettingsConfigDict

import constants


class Settings(BaseSettings):
    JSONBIN_BIN_ID: str
    JSONBIN_ACCESS_KEY: str
    JSONBIN_MASTER_KEY: str
    JSONBIN_ROOT_URL: str

    CLOUDFLARE_ACCOUNT_ID: str
    CLOUDFLARE_API_TOKEN: str

    model_config = SettingsConfigDict(env_file=constants.ENV_FILE_PATH)


settings = Settings()
