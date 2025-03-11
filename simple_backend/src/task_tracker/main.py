from pydantic import BaseModel
from typing import List, Optional

class Task(BaseModel):
    id: int
    title: str
    status: str = "в процессе"
    subtasks: Optional[List[str]] = None
from fastapi import FastAPI, HTTPException
from typing import List

app = FastAPI()

# Хранение задач в оперативной памяти
tasks = []

# Получить все задачи
@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks

# Создать новую задачу
@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    tasks.append(task)
    return task

# Обновить задачу
@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: Task):
    for i, task in enumerate(tasks):
        if task.id == task_id:
            tasks[i] = updated_task
            return updated_task
    raise HTTPException(status_code=404, detail="Задача не найдена")

# Удалить задачу
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    global tasks
    tasks = [task for task in tasks if task.id != task_id]
    return {"message": "Задача удалена"}