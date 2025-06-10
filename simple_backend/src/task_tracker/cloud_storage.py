import requests
import os


class JsonBinStorage:
    def __init__(self):
        self.api_key = os.getenv('JSONBIN_API_KEY')
        self.bin_id = os.getenv('JSONBIN_BIN_ID')
        self.base_url = "https://api.jsonbin.io/v3/b"

    def _get_headers(self):
        return {
            "Content-Type": "application/json",
            "X-Master-Key": self.api_key,
            "x-Bin-Versioning": "False"
        }

    def read_tasks(self):
        """Чтение задач из облачного хранилища"""
        try:
            response = requests.get(
                f"{self.base_url}/{self.bin_id}",
                headers=self._get_headers()
            )
            response.raise_for_status()
            return response.json().get("record", [])
        except requests.exceptions.RequestException:
            return []

    def save_task(self, tasks):
        """Сохранение задач в облачное хранилище"""
        requests.put(
            f"{self.base_url}/{self.bin_id}",
            json=tasks,
            headers=self._get_headers()
        )

    def get_next_id(self, tasks):
        """Генерация следующего ID"""
        return max(task["id"] for task in tasks) + 1 if tasks else 1