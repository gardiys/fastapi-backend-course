from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Pydantic-модель задачи
class Task(BaseModel):
    id: int
    title: str
    completed: bool = False

# Хранилище задач в оперативной памяти
tasks = []

def find_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    return None

# Получение всех задач
@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks

# Создание новой задачи
@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    tasks.append(task)
    return task

# Обновление задачи
@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: Task):
    task = find_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.title = updated_task.title
    task.completed = updated_task.completed
    return task

# Удаление задачи
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    global tasks
    tasks = [task for task in tasks if task.id != task_id]
    return {"message": "Task deleted"}
