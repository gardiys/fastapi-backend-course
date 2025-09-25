from fastapi import FastAPI
from pydantic import BaseModel
import json

app = FastAPI()

class Task(BaseModel):
    id: int
    title: str
    completed: bool = False

# Функции для работы с файлом
def load_tasks():
    try:
        with open("tasks.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Task(**task) for task in data]
    except:
        # Если файла нет, создаем начальные задачи
        initial_tasks = [
            {"id": 1, "title": "купить молоко", "completed": False},
            {"id": 2, "title": "позавтракать", "completed": True},
            {"id": 3, "title": "позвонить дедушке", "completed": False}
        ]
        with open("tasks.json", "w", encoding="utf-8") as f:
            json.dump(initial_tasks, f, ensure_ascii=False, indent=2)
        return [Task(**task) for task in initial_tasks]

def save_tasks(tasks):
    with open("tasks.json", "w", encoding="utf-8") as f:
        data = [task.dict() for task in tasks]
        json.dump(data, f, ensure_ascii=False, indent=2)

# GET /tasks - получить все задачи
@app.get("/tasks")
def get_tasks():
    return load_tasks()

# POST /tasks - создать новую задачу
@app.post("/tasks")
def create_task(title: str):
    tasks = load_tasks()
    new_id = max(task.id for task in tasks) + 1
    new_task = Task(id=new_id, title=title, completed=False)
    tasks.append(new_task)
    save_tasks(tasks)
    return new_task

# PUT /tasks/{id} - обновить задачу
@app.put("/tasks/{task_id}")
def update_task(task_id: int, title: str = None, completed: bool = None):
    tasks = load_tasks()
    for task in tasks:
        if task.id == task_id:
            if title is not None:
                task.title = title
            if completed is not None:
                task.completed = completed
            save_tasks(tasks)
            return task
    return {"error": "Задача не найдена"}

# DELETE /tasks/{id} - удалить задачу
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    tasks = load_tasks()
    for i, task in enumerate(tasks):
        if task.id == task_id:
            deleted_task = tasks.pop(i)
            save_tasks(tasks)
            return {"message": f"Задача '{deleted_task.title}' удалена"}
    return {"error": "Задача не найдена"}