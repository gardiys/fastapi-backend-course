from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from storage import CloudStorage
from llm_service import LLMService


app = FastAPI()

JSONBIN_API_KEY = '$2a$10$3xXzKoQl9Akw7iQuxSY7Debk9qvfKv7cqkKJ9qUWURQKEQvy7j4Gq'
CLOUDFLARE_API_KEY = '5MrpalKTY6FkRSQ2ak02YhG-EGkxgVAz7MyDmftZ'

tasks = CloudStorage(JSONBIN_API_KEY, '67db396b8561e97a50ef5ca1')
llm = LLMService(CLOUDFLARE_API_KEY)

class Task(BaseModel):
    id: Optional[int] = None
    text: str
    completed: bool = False
    solution: Optional[str] = None



@app.get("/tasks", response_model=List[Task])
def get_tasks():
    """Получить список всех задач."""
    return tasks.load_tasks()

@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    """Создать новую задачу."""
    
    current_tasks = tasks.load_tasks()
    
    solution = llm.get_task_solution(task.text)
    if solution:
        task.solution = solution
    
    #task.id = len(current_tasks) + 1
    current_tasks.append(task.model_dump())
    tasks.save_tasks(current_tasks)
    
    return task

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: Task):
    """Обновить существующую задачу."""
    current_tasks = tasks.load_tasks()
    
    for t in current_tasks:
        if t["id"] == task_id:
            t.update(task.model_dump(exclude_unset=True))
            tasks.save_tasks(current_tasks)
            return t
    
    raise HTTPException(status_code=404, detail="Задача не найдена")

@app.delete("/tasks/{task_id}", response_model=Task)
def delete_task(task_id: int):
    """Удалить задачу."""
    current_tasks = tasks.load_tasks()
    
    for index, task in enumerate(current_tasks):
        if task["id"] == task_id:
            deleted_task = task
            current_tasks.pop(index)
            tasks.save_tasks(current_tasks)
            return deleted_task
    
    raise HTTPException(status_code=404, detail="Задача не найдена")
