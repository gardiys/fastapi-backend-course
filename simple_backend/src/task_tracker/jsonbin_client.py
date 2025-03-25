import os
from dotenv import load_dotenv
from base_http_client import BaseHTTPClient

load_dotenv()


class JSONBinConfig:
    """Конфигурация для работы с JSONBin.io."""

    def __init__(self):
        self.api_key = os.getenv("JSONBIN_API_KEY")
        self.bin_id = os.getenv("JSONBIN_BIN_ID")

        if not all([self.api_key, self.bin_id]):
            raise ValueError("❌ Ошибка: Отсутствуют переменные окружения в .env!")


class JSONBinClient(BaseHTTPClient):
    """Клиент для работы с JSONBin.io."""

    def __init__(self, config: JSONBinConfig):
        super().__init__()
        self.config = config
        self.api_url = f"https://api.jsonbin.io/v3/b/{self.config.bin_id}"

    def get_headers(self) -> dict:
        """Возвращает заголовки запроса."""
        return {
            "X-Master-Key": self.config.api_key,
            "Content-Type": "application/json",
        }

    def load_tasks(self):
        """Загружает задачи из JSONBin.io."""
        response = self.request("GET", self.api_url)
        return response.get("record", [])

    def save_tasks(self, tasks):
        """Сохраняет задачи в JSONBin.io."""
        self.request("PUT", self.api_url, {"record": tasks})
