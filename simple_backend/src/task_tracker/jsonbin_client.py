import os
from dotenv import load_dotenv
from base_http_client import BaseHTTPClient

load_dotenv()


class JSONBinClient(BaseHTTPClient):
    """Клиент для работы с JSONBin.io"""

    API_URL = "https://api.jsonbin.io/v3/b/67cb2c8ce41b4d34e4a280c7"

    def __init__(self):
        self.api_key = os.getenv("JSONBIN_API_KEY")
        if not self.api_key:
            raise ValueError("API-ключ JSONBin.io не найден! Проверь .env файл.")

    def get_headers(self) -> dict:
        """Возвращает заголовки запроса."""
        return {
            "X-Master-Key": self.api_key,
            "Content-Type": "application/json",
        }

    def load_tasks(self):
        """Загружает задачи из JSONBin.io."""
        response = self.request("GET", self.API_URL)
        return response.get("record", {}).get("record", [])

    def save_tasks(self, tasks):
        """Сохраняет задачи в JSONBin.io."""
        self.request("PUT", self.API_URL, {"record": tasks})
