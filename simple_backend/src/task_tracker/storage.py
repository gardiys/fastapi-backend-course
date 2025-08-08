import json
import os
from typing import List

DATA_FILE = "tasks.json"

class FileStorage:
    @staticmethod
    def load_tasks() -> List[dict]:
        if not os.path.exists(DATA_FILE):
            return []
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    @staticmethod
    def save_tasks(tasks: List[dict]):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2)