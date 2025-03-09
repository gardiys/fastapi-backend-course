import json
from typing import List, Optional
from pathlib import Path

class TaskStorage:
    def __init__(self, file_path: str = "tasks.json"):
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            self.file_path.write_text("[]")

    def read_tasks(self) -> List[dict]:
        with open(self.file_path, "r") as file:
            return json.load(file)

    def write_tasks(self, tasks: List[dict]):
        with open(self.file_path, "w") as file:
            json.dump(tasks, file, indent=4)