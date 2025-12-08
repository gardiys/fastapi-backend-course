from fastapi import FastAPI, HTTPException
from typing import List, Dict
from jsonbin_storage import JSONBinStorage


app = FastAPI()

storage = JSONBinStorage(
    bin_id="69357644d0ea881f40189c35", 
    api_key="$2a$10$ScuQ39x39M1YXbyYLD2mLeldzClKkweUfdiq/gLJYVfcVc70da5pW"  
)


@app.get("/tasks", response_model=List[Dict])
def get_tasks():
    return storage.get_tasks()


@app.post("/tasks", response_model=Dict)
def create_task(task: Dict):
    return storage.create_task(task)


@app.put("/tasks/{task_id}", response_model=Dict)
def update_task(task_id: int, updated_task: Dict):
    try:
        return storage.update_task(task_id, updated_task)
    except ValueError:
        raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    try:
        storage.delete_task(task_id)
        return {"detail": "Task deleted"}
    except ValueError:
        raise HTTPException(status_code=404, detail="Task not found")

