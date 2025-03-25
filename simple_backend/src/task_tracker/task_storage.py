import requests
from typing import List, Dict
import json
from fastapi import HTTPException

class TaskStorage:
    def __init__(self, api_key: str, bin_id: str):
        self.api_key = api_key
        self.bin_id = bin_id
        self.base_url = f"https://api.jsonbin.io/v3/b/{bin_id}"

    def load_tasks(self) -> List[Dict]:
        """Загружает задачи из jsonbin.io и преобразует их в список словарей."""
        headers = {
            "X-Master-Key": self.api_key
        }
        response = requests.get(self.base_url, headers=headers)
        tasks = response.json().get("record", [])

        if isinstance(tasks, list) and all(isinstance(t, str) for t in tasks):
            tasks = [json.loads(t) for t in tasks]

        return tasks


    def save_tasks(self, tasks: List[Dict]):
        """Сохраняет задачи в jsonbin.io."""
        headers = {
            "Content-Type": "application/json",
            "X-Master-Key": self.api_key
        }
        response = requests.put(self.base_url, json=tasks, headers=headers)



