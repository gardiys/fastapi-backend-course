from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

app = FastAPI(title="Task Tracker", description="Simple task management API")

class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress" 
    DONE = "done"

class TaskCreate(BaseModel):
    title: str
    status: TaskStatus = TaskStatus.TODO

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[TaskStatus] = None

class Task(BaseModel):
    id: int
    title: str
    status: TaskStatus

tasks_db: List[Task] = []
next_id = 1

@app.get("/")
def read_root():
    return {"message": "Task Tracker API"}

@app.get("/tasks", response_model=List[Task])
def get_tasks():
    """Получить список всех задач"""
    return tasks_db

@app.post("/tasks", response_model=Task)
def create_task(task: TaskCreate):
    """Создать новую задачу"""
    global next_id
    
    new_task = Task(
        id=next_id,
        title=task.title,
        status=task.status
    )
    
    tasks_db.append(new_task)
    next_id += 1
    
    return new_task

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    """Получить задачу по ID"""
    for task in tasks_db:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_update: TaskUpdate):
    """Обновить задачу"""
    for i, task in enumerate(tasks_db):
        if task.id == task_id:
            if task_update.title is not None:
                task.title = task_update.title
            if task_update.status is not None:
                task.status = task_update.status
            
            tasks_db[i] = task
            return task
    
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    """Удалить задачу"""
    for i, task in enumerate(tasks_db):
        if task.id == task_id:
            deleted_task = tasks_db.pop(i)
            return {"message": f"Task '{deleted_task.title}' deleted successfully"}
    
    raise HTTPException(status_code=404, detail="Task not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
