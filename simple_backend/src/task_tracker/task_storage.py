# не используется. локальное хранение задач заменено на gist_storage.py

from .storage_client import StorageClient
from pathlib import Path
from typing import Any
import json

class TaskStorage(StorageClient):
    def __init__(self, file_path: str):
	self.file_path = Path(file_path)
	if not self.file_path.exists():
	    self.save_data([])

    def load_data(self) -> list[dict[str, Any]]:
        with self.file_path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def save_data(self, data: Any):
        with self.file_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
