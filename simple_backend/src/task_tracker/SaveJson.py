import json
from typing import List
from model import Task
import requests
from fastapi import HTTPException

from BaseHTTPClient import BaseHTTPClient


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


class SaveJsonDB(BaseHTTPClient):
    def __init__(self, base_url: str, timeout: int):
        super().__init__(base_url, timeout)

    def json_to_task(self,data:dict|list[dict])->Task|list[Task]:
        if isinstance(data, list):
            return [Task.model_validate(item) for item in data]
        return Task.model_validate(data)





    def load_tasks(self) -> List[Task]:
        try:
            tasks_json = self.get("tasks")
            return self.json_to_task(tasks_json)
        except requests.exceptions.RequestException as e:
            raise e

    def update_task_id(self,id:int,task:Task)->Task:
        try:
            data = task.model_dump()
            task_json = self.put(f"tasks/{id}",data)
            return self.json_to_task(task_json)
        except requests.exceptions.RequestException:
            raise HTTPException(status_code=404, detail="Task not found")

    def delete_task_id(self,id:int)->Task:
        try:
            task_json = self.delete(f"tasks/{id}")
            return self.json_to_task(task_json)
        except requests.exceptions.RequestException:
            raise HTTPException(status_code=404, detail="Task not found")

    def create_task(self,task:Task) -> Task:
        try:
            data = task.model_dump()
            task_json = self.post("tasks",data)
            return self.json_to_task(task_json)
        except requests.exceptions.RequestException as e:
            raise e



