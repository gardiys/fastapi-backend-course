import json
from typing import List
from model import Task

class Save_Json:
    def __init__(self,file_path):
        self.file_path = file_path

    def load_json(self) -> List[dict]:
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print("Error: File not found")
            return []
        except json.JSONDecoder:
            print("Error:Failed parsing JSON")
            return []

    def save_json(self,data):
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def json_to_task(self,json_data: List[dict]) -> list[Task]:
        return [Task(**item) for item in json_data]

    def task_to_json(self,tasks_: List[Task]) -> List[dict]:
        return [task.dict() for task in tasks_]



