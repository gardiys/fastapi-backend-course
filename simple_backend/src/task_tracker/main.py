from fastapi import FastAPI, HTTPException
import json

app = FastAPI()

TASK_FILE = "tasks.json"


class Task:
    def __init__(self, id, title, status="To Do"):
        self.id = id
        self.title = title
        self.status = status


class TaskFileManager:
    def __init__(self, task_file):
        self.task_file = task_file
        self.tasks = self._load_tasks()
        self.task_id_counter = self._get_next_task_id()

    def _load_tasks(self):
        try:
            with open(self.task_file, "r") as f:
                tasks_data = json.load(f)
                tasks = []
                max_id = 0
                for task_data in tasks_data:
                    task = Task(
                        id=task_data["id"],
                        title=task_data["title"],
                        status=task_data["status"],
                    )
                    tasks.append(task)
                    if task.id > max_id:
                        max_id = task.id
                return tasks
        except FileNotFoundError:
            return []

    def _save_tasks(self):
        with open(self.task_file, "w") as f:
            tasks_list_for_json = []
            for task in self.tasks:
                tasks_list_for_json.append(
                    {"id": task.id, "title": task.title, "status": task.status}
                )
            json.dump(tasks_list_for_json, f, indent=4)

    def _get_next_task_id(self):
        if not self.tasks:
            return 1
        else:
            return max(task.id for task in self.tasks) + 1

    def get_tasks(self):
        return [
            {"id": task.id, "title": task.title, "status": task.status}
            for task in self.tasks
        ]

    def create_task(self, task_data):
        new_task = Task(id=self.task_id_counter, title=task_data["title"])
        self.tasks.append(new_task)
        self._save_tasks()
        self.task_id_counter += 1
        return {"id": new_task.id, "title": new_task.title, "status": new_task.status}

    def update_task(self, task_id, task_data):
        for task in self.tasks:
            if task.id == task_id:
                if "title" in task_data:
                    task.title = task_data["title"]
                if "status" in task_data:
                    task.status = task_data["status"]
                self._save_tasks()
                return {"id": task.id, "title": task.title, "status": task.status}
        raise HTTPException(status_code=404, detail="Task not found")

    def delete_task(self, task_id):
        original_tasks_count = len(self.tasks)
        self.tasks = [task for task in self.tasks if task.id != task_id]
        if len(self.tasks) == original_tasks_count:
            raise HTTPException(status_code=404, detail="Task not found")
        self._save_tasks()
        return {"message": "Task deleted"}


task_file_manager = TaskFileManager(TASK_FILE)


@app.get("/tasks")
async def get_tasks():
    return task_file_manager.get_tasks()


@app.post("/tasks")
async def create_task(task_data: dict):
    return task_file_manager.create_task(task_data)


@app.put("/tasks/{task_id}")
async def update_task(task_id: int, task_data: dict):
    return task_file_manager.update_task(task_id, task_data)


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    return task_file_manager.delete_task(task_id)
