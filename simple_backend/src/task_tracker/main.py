from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os

app = FastAPI()
file_name = 'tasks.json'

class Task(BaseModel):
    name: str
    status: str

    def __repr__(self):
        return f"Task(name={self.name}, status={self.status})"

class TaskTracker:
    def __init__(self, file_name):
        self.file_name = file_name
        if not os.path.exists(self.file_name):
            with open(self.file_name, 'w', encoding='utf-8') as file:
                json.dump({}, file)

    def read_json(self):
        try:
            with open(self.file_name, 'r', encoding='utf-8') as file:
                return json.load(file)
        except json.JSONDecodeError:
            return {}
        except Exception as err:
            return {'error': str(err)}

    def add_json(self, task):
        try:
            info = self.read_json()
            task_id = max(map(int, info.keys()), default=0) + 1
            info[str(task_id)] = task.dict()
            with open(self.file_name, 'w', encoding='utf-8') as file:
                json.dump(info, file, indent=4, ensure_ascii=False)
                return {'message': 'задача сохранена'}
        except Exception as err:
            return {'error': str(err)}

    def delete_json(self, task_id):
        info = self.read_json()
        if str(task_id) not in info:
            raise HTTPException(status_code=404, detail='task not found')
        del info[str(task_id)]
        try:
            with open(self.file_name, 'w', encoding='utf-8') as file:
                json.dump(info, file, indent=4, ensure_ascii=False)
                return {'message': 'задача удалена'}
        except Exception as err:
            return {'error': str(err)}

    def update_json(self, task_id, task):
        info = self.read_json()
        if str(task_id) not in info:
            raise HTTPException(status_code=404, detail='task not found')
        info[str(task_id)] = task.dict()
        try:
            with open(self.file_name, 'w', encoding='utf-8') as file:
                json.dump(info, file, indent=4, ensure_ascii=False)
                return {'message': 'задача сохранена'}
        except Exception as err:
            return {'error': str(err)}

tracker = TaskTracker(file_name)

@app.get("/tasks")
def get_tasks():
    return tracker.read_json()

@app.post("/tasks")
def create_task(task: Task):
    return tracker.add_json(task)

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    return tracker.update_json(task_id, task)

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    return tracker.delete_json(task_id)


