from fastapi import FastAPI
from fastapi import HTTPException
from pathlib import Path
import json

app = FastAPI()

class TaskStorage:
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            self.save_data([])

    def load_data(self):
        with open(self.file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_data(self, data):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

class TaskManager:
    def __init__(self, storage: TaskStorage):
        self.storage = storage

    def get_all_tasks(self):
        return self.storage.load_data()

    def create_task(self, title: str):
        tasks = self.storage.load_data()
        new_id = max([t["id"] for t in tasks], default = 0) + 1
        new_task = {"id": new_id, "title": title, "status": "in work"}
        tasks.append(new_task)
        self.storage.save_data(tasks)
        return new_task

    def update_task(self, task_id, title: str = None, status: str = None):
        tasks = self.storage.load_data()
        for task in tasks:
            if task["id"] == task_id:
                if title:
                    task["title"] = title
                if status:
                    task["status"] = status
                self.storage.save_data(tasks)
                return task
        raise HTTPException(status_code=404, detail="Task not found")

    def delete_task(self, task_id: int):
        tasks = self.storage.load_data()
        for task in tasks:
            if task["id"] == task_id:
                tasks.remove(task)
                self.storage.save_data(tasks)
                return {"message": "Task deleted"}
        raise HTTPException(status_code=404, detail="Task not found")

storage = TaskStorage("tasks.json")
task_manager = TaskManager(storage)

@app.get("/tasks")
def get_tasks():
    return task_manager.get_all_tasks()

@app.post("/tasks")
def create_task(title: str):
    return task_manager.create_task(title)

@app.put("/tasks/{task_id}")
def update_task(task_id: int, title: str = None, status: str = None):
    return task_manager.update_task(task_id, title, status)

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    return task_manager.delete_task(task_id)

