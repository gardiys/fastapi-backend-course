from fastapi import FastAPI, HTTPException
from task_tracker.gist_storage import GistStorage

app = FastAPI()
storage = GistStorage()

@app.get("/tasks")
def get_tasks():
    try:
        return storage.load_data()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tasks")
def create_task(title: str):
    try:
        tasks = storage.load_data()
        new_id = max([t["id"] for t in tasks], default=0) + 1
        new_task = {"id": new_id, "title": title, "status": "in work"}
        tasks.append(new_task)
        storage.save_data(tasks)
        return new_task
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/tasks/{task_id}")
def update_task(task_id: int, title: str = None, status: str = None):
    try:
        tasks = storage.load_data()
        for task in tasks:
            if task["id"] == task_id:
                if title:
                    task["title"] = title
                if status:
                    task["status"] = status
                storage.save_data(tasks)
                return task
        raise HTTPException(status_code=404, detail="Task not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    try:
        tasks = storage.load_data()
        for task in tasks:
            if task["id"] == task_id:
                tasks.remove(task)
                storage.save_data(tasks)
                return {"message": "Task deleted"}
        raise HTTPException(status_code=404, detail="Task not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

