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

def read_json():
    if not os.path.exists(file_name):
        return {}
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError:
        return {}
    except Exception as err:
        return {'error': str(err)}

def add_json(task):
    try:
        info = read_json()
        task_id = max(map(int, info.keys()), default=0) + 1
        info[str(task_id)] = task.dict()
        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(info, file, indent=4, ensure_ascii=False)
            return {'message': 'задача сохранена'}
    except Exception as err:
        return {'error': str(err)}

def delete_json(task_id):
    info = read_json()
    if str(task_id) not in info:
        raise HTTPException(status_code=404, detail='task not found')
    del info[str(task_id)]
    try:
        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(info, file, indent=4, ensure_ascii=False)
            return {'message': 'задача удалена'}
    except Exception as err:
        return {'error': str(err)}

def update_json(task_id, task):
    info = read_json()
    if str(task_id) not in info:
        raise HTTPException(status_code=404, detail='task not found')
    info[str(task_id)] = task.dict()
    try:
        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(info, file, indent=4, ensure_ascii=False)
            return {'message': 'задача сохранена'}
    except Exception as err:
        return {'error': str(err)}

@app.get("/tasks")
def get_tasks():
    return read_json()

@app.post("/tasks")
def create_task(task: Task):
    return add_json(task)

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    return update_json(task_id, task)

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    return delete_json(task_id)


