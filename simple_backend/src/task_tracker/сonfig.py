import os

from dotenv import load_dotenv


class Config:
    def __init__(self):
        load_dotenv()

    def get_ai_agent(self) -> dict:
        ai_agent = {
            "API_BASE_URL": os.getenv("API_BASE_URL"),
            "API_TOKEN": os.getenv("API_TOKEN"),
            "model": os.getenv("model"),
        }
        return ai_agent

    def get_url_DB(self) -> str:
        return os.getenv("DB_URL")
