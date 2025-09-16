from fastapi import FastAPI, Query, HTTPException
from storage import FileStorage

app = FastAPI()
storage = FileStorage()

@app.get("/tasks")
def get_tasks():
    return storage.get_all_tasks()

@app.post("/tasks")
def create_task(
    task: str = Query(...),
    status: str = Query(...)
):
    if isinstance(status, str) and isinstance(task, str):
        new_task = storage.create_task(task, status)
        return new_task
    else:
        raise ValueError('status and task only str')

@app.put("/tasks/{task_id}")
def update_task(
    task_id: int,
    new_name: str = Query(...),
    new_status: str = Query(...)
):
    if isinstance(new_status, str) and isinstance(new_name, str) and isinstance(task_id, int):
        updated_task = storage.update_task(task_id, new_name, new_status)
        if updated_task:
            return updated_task
        raise HTTPException(status_code=404, detail="Task not found")
    else:
        raise ValueError('name and status only str and id only int')

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    if isinstance(task_id, int):
        deleted_task = storage.delete_task(task_id)
        if deleted_task:
            return {"message": "Task deleted", "task": deleted_task}
        raise HTTPException(status_code=404, detail="Task not found")
    else:
        raise ValueError('task_id only int')