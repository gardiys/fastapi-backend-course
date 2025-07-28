import json
from typing import List
from model import Task
import requests
from fastapi import HTTPException

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


class SaveJsonDB:
    def __init__(self, url):
        self.url = url
    def load_tasks(self) -> List[Task]:
        try:
            response = requests.get(f'{self.url}tasks',timeout=5)
            response.raise_for_status()
            return [Task.model_validate(item) for item in response.json()]
        except requests.exceptions.RequestException as e:
            raise e

    def update_task_id(self,id:int,task:Task)->Task:
        try:
            data = task.model_dump()
            response = requests.put(f'{self.url}tasks/{id}',json=data,timeout=5)
            response.raise_for_status()
            return Task.model_validate(response.json())
        except requests.exceptions.RequestException:
            raise HTTPException(status_code=404, detail="Task not found")

    def delete_task_id(self,id:int)->Task:
        try:
            response = requests.delete(f"{self.url}tasks/{id}")
            response.raise_for_status()
            return Task.model_validate(response.json())
        except requests.exceptions.RequestException:
            raise HTTPException(status_code=404, detail="Task not found")

    def create_task(self,task:Task) -> Task:
        try:
            data = task.model_dump()
            response = requests.post(f"{self.url}tasks",json=data,timeout=5)
            response.raise_for_status()
            return Task.model_validate(response.json())
        except requests.exceptions.RequestException as e:
            raise e



