from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Task(BaseModel):
    id:int
    title:str
    status:str

tasks = []

@app.get("/tasks",response_model=List[Task])
def get_tasks():
    return tasks

@app.post("/tasks")
def create_task(task:Task):
    tasks.append(task)
    return tasks

@app.put("/tasks/{task_id}",response_model=Task)
def update_task(task_id: int,updated_task:Task):
    for index in range(len(tasks)):
        if tasks[index].id == task_id:
            tasks[index] = updated_task
            return updated_task
        raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for index in range(len(tasks)):
        if tasks[index].id == task_id:
            return tasks.pop(index)
        raise HTTPException(status_code=404,detail="Task not found")

