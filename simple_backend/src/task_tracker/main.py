from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv
from cloud_storage import JsonBinStorage

load_dotenv()

app = FastAPI()
storage = JsonBinStorage()


class Task(BaseModel):
    id: int
    title: str
    status: str


# API
@app.get("/tasks", response_model=list[Task])
def get_tasks():
    """Возвращаем список задач"""
    tasks = storage.read_tasks()
    return [Task(**task) for task in tasks]


@app.post("/tasks", response_model=Task)
def create_task(title: str, status: str = "pending"):
    """Создаем новую задачу"""
    tasks = storage.read_tasks()
    new_task = {
        "id": storage.get_next_id(tasks),
        "title": title,
        "status": status
    }
    tasks.append(new_task)
    if not storage.save_task(tasks):
        raise HTTPException(status_code=500, detail="Failed to save task")
    return Task(**new_task)


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, title: Optional[str] = None, status: Optional[str] = None):
    """Обновляет задачу"""
    tasks = storage.read_tasks()
    task_found = False

    for task in tasks:
        if task["id"] == task_id:
            task_found = True
            if title is not None:
                task["title"] = title
            if status is not None:
                task["status"] = status
            break
    
    if not task_found:
        raise HTTPException(status_code=500, detail="Task not found")
    
    if not storage.save_task(tasks):
        raise HTTPException(status_code=500, detail="Failed to update task")
    
    return Task(**task)
    


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    """Удаляет задачу"""
    tasks = storage.read_tasks()
    length = len(tasks)

    updated_tasks = [task for task in tasks if task["id"] != task_id]

    if len(updated_tasks) == length:
        raise HTTPException(status_code=404, detail="Task not found")

    if not storage.save_task(updated_tasks):
        raise HTTPException(status_code=404, detail="Failed to delete task")

    return {"message": "Task deleted successfully"}
