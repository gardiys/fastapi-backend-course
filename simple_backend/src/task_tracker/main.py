from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()

class Task(BaseModel):
    text: str
    is_done: bool = False  

# Конфигурация JSONBin.io
headers = {
    'Content-Type': 'application/json',
    'X-Master-Key': '$2a$10$92anMMSpReZf03/15uRLVeWseU19ToTVWdu5qHUVY5p0M.uc9BNNq',  
    'X-Access-Key': '$2a$10$bag0phEtSGHeSS8uovM9MOU3bRW.7piFdMY5TEEEGeHlq1GSoA4P6',
}

BIN_ID = '686d58048960c979a5b952d9'
URL = f'https://api.jsonbin.io/v3/b/{BIN_ID}'

# Инициализация хранилища
try:
    response = requests.get(f"{URL}/latest", headers=headers)
    tasks = [Task(**item) for item in response.json()['record']]
except:
    tasks = []


@app.on_event("startup")
def verify_connection():
    try:
        response = requests.get(
            f"https://api.jsonbin.io/v3/b/{BIN_ID}",
            headers={'X-Master-Key': '$2a$10$92anMMSpReZf03/15uRLVeWseU19ToTVWdu5qHUVY5p0M.uc9BNNq'}
        )
        print('Подключение к JSONBin прошло успешно')
        assert response.status_code == 200
    except Exception as e:
        print("❌ Ошибка подключения к JSONBin:", str(e))
        raise

@app.get("/tasks", response_model=list[Task])
def list_tasks(limit: int = 6):
    return tasks[:limit]

@app.post("/tasks", response_model=list[Task])
def create_task(task: Task):
    tasks.append(task)
    response = requests.put(URL, json=[t.dict() for t in tasks], headers=headers)
    if response.status_code != 200:
        tasks.pop()  # Откат при ошибке
        raise HTTPException(500, detail=f"JSONBin error: {response.text}")
    return tasks

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    try:
        return tasks[task_id]
    except IndexError:
        raise HTTPException(404, detail='Task not found')

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    try:
        deleted = tasks.pop(task_id)
        response = requests.put(URL, json=[t.dict() for t in tasks], headers=headers)
        if response.status_code != 200:
            tasks.insert(task_id, deleted)  # Откат при ошибке
            raise HTTPException(500, detail="Failed to update cloud storage")
        return {"status": "deleted"}
    except IndexError:
        raise HTTPException(404, detail='Task not found')
