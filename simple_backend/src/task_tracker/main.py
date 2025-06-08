from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Task(BaseModel):
    id: int
    title: str
    status: str

tasks_db = []
current_id = 1

@app.get("/tasks", response_model=list[Task])
def get_tasks():
    """Возвращаем список задач"""
    return tasks_db

@app.post("/tasks", response_model=Task)
def create_task(title: str, status: str = "pending"):
    """Создаем новую задачу"""
    global current_id
    task = Task(id=current_id, title=title, status=status)
    tasks_db.append(task)
    current_id += 1
    return task

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, title: Optional[str] = None, status: Optional[str] = None):
    """Обновляет информацию о задаче"""
    for task in tasks_db:
        if task.id == task_id:
            if title is not None:
                task.title = title
            if status is not None:
                task.status = status
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    """Удаляет задачу"""
    global tasks_db
    length = len(tasks_db)
    tasks_db = [task for task in tasks_db if task.id != task_id]
    if len(tasks_db) == length:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}
