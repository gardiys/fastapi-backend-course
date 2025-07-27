from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from typing import List
import json

app = FastAPI()

class Task(BaseModel):
    id:int
    title:str
    status:str


FILE_PATH = "tasks.json"

def load_json() -> List[dict]:
    try:
        with open(FILE_PATH,'r',encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print("Error: Не найден фаил")
        return []
    except json.JSONDecoder:
        raise HTTPException(status_code=500,detail="Ошибка при парсинге JSON")

def save_json(data):
    with open(FILE_PATH,'w',encoding='utf-8') as file:
        json.dump(data,file,ensure_ascii=False,indent=4)

def json_to_task(json_data:List[dict])-> list[Task]:
    return [Task(**item) for item in json_data]

def task_to_json(tasks_:List[Task])->List[dict]:
    return [task.dict() for task in tasks_]




@app.get("/tasks",response_model=List[Task])
def get_tasks():
    json_data = load_json()
    return json_to_task(json_data)

@app.post("/tasks")
def create_task(task:Task):
    json_data = load_json()
    json_data.append(task.dict())
    save_json(json_data)
    return task

@app.put("/tasks/{task_id}",response_model=Task)
def update_task(task_id: int,updated_task:Task):
    json_data = load_json()
    tasks = json_to_task(json_data)
    for index in range(len(tasks)):
        if tasks[index].id == task_id:
            tasks[index] = updated_task
            save_json(task_to_json(tasks))
            return updated_task
        raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    json_data = load_json()
    tasks = json_to_task(json_data)
    for index in range(len(tasks)):
        if tasks[index].id == task_id:
            task_del = tasks.pop(index)
            save_json(task_to_json(tasks))
            return task_del
        raise HTTPException(status_code=404,detail="Task not found")

