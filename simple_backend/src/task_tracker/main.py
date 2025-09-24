from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Task(BaseModel):
    id: int
    title: str
    completed: bool = False

tasks = [
    Task(id=1, title="купить молоко", completed=False),
    Task(id=2, title="позавтракать", completed=True),
    Task(id=3, title="позвонить дедушке", completed=False)
]

# GET /tasks - получить все задачи
@app.get("/tasks")
def get_tasks():
    return tasks

# POST /tasks - создать новую задачу
@app.post("/tasks")
def create_task(title: str):
    new_id = max(task.id for task in tasks) + 1
    new_task = Task(id=new_id, title=title, completed=False)
    tasks.append(new_task)
    return new_task

# PUT /tasks/{id} - обновить задачу
@app.put("/tasks/{task_id}")
def update_task(task_id: int, title: str = None, completed: bool = None):
    for task in tasks:
        if task.id == task_id:
            if title is not None:
                task.title = title
            if completed is not None:
                task.completed = completed
            return task
    return {"error": "Задача не найдена"}

# DELETE /tasks/{id} - удалить задачу
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for i, task in enumerate(tasks):
        if task.id == task_id:
            deleted_task = tasks.pop(i)
            return {"message": f"Задача '{deleted_task.title}' удалена"}
    return {"error": "Задача не найдена"}