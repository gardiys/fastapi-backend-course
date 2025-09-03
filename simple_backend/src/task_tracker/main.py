from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr, Field, field_validator, ValidationError
from db import list_db
from typing import List

from utils import TaskController, Worker_AI

app = FastAPI()
task_controller = TaskController(list_db)

class Task(BaseModel):
    id: int
    title: str = Field(default=..., min_length=1, max_length=50, description="Название задачи, от 1 до 50 символов")
    text: str = Field(default=..., min_length=1, max_length=500, description="Текст задачи, от 1 до 500 символов")
    status: str = Field(default=..., min_length=1, max_length=50, description="Статус задачи, от 1 до 50 символов")

@app.get("/tasks")
def get_tasks() -> List[Task]:
    list_task = task_controller.get_all_task()
    print('TASK', list_task)
    tasks = [Task(**task) for task in list_task]       
    return tasks
    

@app.post("/tasks")
def create_task(task: Task):
    ai = Worker_AI()
    task.text += f'\nРешение: {ai.creating_solution_to_task(task.text)}\n'
    task_controller.add_task(task.model_dump())
    return task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    existing_task = task_controller.update_task(task_id, task)
    if existing_task:
        return {"message": f"Task with id {task_id} update successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    deleted = task_controller.delete_task(task_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return {
        "message": f"Task with id {task_id} deleted successfully",
        "deleted_id": task_id
    }
