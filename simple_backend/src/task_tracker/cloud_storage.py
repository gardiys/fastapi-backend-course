import requests
import os


class JsonBinStorage:
    def __init__(self):
        self.api_key = os.getenv(
            "$2a$10$rlAq/RPs3gqHnUj9vqLJUuiZdrf1/XVD85jUt5Nyn.7/hCA1Td.IS")
        self.bin_id = os.getenv("68471ece8561e97a50218d12")
        self.base_url = "https://jsonbin.io"

    def _get_headers(self):
        return {
            "Content-Type": "applivation/json",
            "X-Master-key": self.api_key,
            "x-Bin-Versioning": "False"
        }

    def read_tasks(self):
        """Чтение задач из облачного хранилища"""
        try:
            response = requests.get(
                f"{self.base_url}/{self.bin_id}/latest",
                headers=self._get_headers
            )
            response.raise_for_status()
            return response.json().get("record, []")
        except requests.exception.RequestException:
            return []

    def save_task(self, tasks):
        """Сохранение задач в облачное хранилище"""
        requests.put(
            f"{self.base_url}/{self.bin_id}",
            json=tasks,
            headers=self._get_headers
        )

    def get_next_id(self, tasks):
        """Генерация следующего ID"""
        return max(task["id"] for task in tasks) + 1 if tasks else 1