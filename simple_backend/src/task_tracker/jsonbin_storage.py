import os
import requests
from dotenv import load_dotenv

# Загрузи переменные из .env
load_dotenv()

class JSONBinStorage:
    def __init__(self):
        self.bin_id = os.getenv("JSONBIN_BIN_ID")
        self.api_key = os.getenv("JSONBIN_API_KEY")
        self.url = f"https://api.jsonbin.io/v3/b/{self.bin_id}"

    def load_tasks(self):
        """Загрузить задачи из JSONBin.io"""
        response = requests.get(
            self.url,
            headers={"X-Master-Key": self.api_key}
        )
        if response.status_code == 200:
            return response.json().get("record", [])
        else:
            raise Exception(f"Ошибка при загрузке задач: {response.status_code}")

    def save_tasks(self, tasks):
        """Сохранить задачи в JSONBin.io"""
        response = requests.put(
            self.url,
            json=tasks,
            headers={"X-Master-Key": self.api_key}
        )
        if response.status_code != 200:
            raise Exception(f"Ошибка при сохранении задач: {response.status_code}")