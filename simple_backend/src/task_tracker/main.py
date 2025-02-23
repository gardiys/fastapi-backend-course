from fastapi import FastAPI, HTTPException
import json

app = FastAPI()

TASK_FILE = "tasks.json"


class Task:
    def __init__(self, id, title, status="To Do"):
        self.id = id
        self.title = title
        self.status = status


def load_tasks():
    try:
        with open(TASK_FILE, "r") as f:
            tasks_data = json.load(f)
            tasks = []
            global task_id_counter
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
            task_id_counter = max_id + 1
            return tasks
    except FileNotFoundError:
        return []


def save_tasks(tasks_to_save):
    with open(TASK_FILE, "w") as f:
        tasks_list_for_json = []
        for task in tasks_to_save:
            tasks_list_for_json.append(
                {"id": task.id, "title": task.title, "status": task.status}
            )
        json.dump(tasks_list_for_json, f, indent=4)


tasks = load_tasks()
task_id_counter = 1 if not tasks else max(task.id for task in tasks) + 1


@app.get("/tasks")
async def get_tasks():
    return [
        {"id": task.id, "title": task.title, "status": task.status} for task in tasks
    ]


@app.post("/tasks")
async def create_task(task_data: dict):
    global task_id_counter
    new_task = Task(id=task_id_counter, title=task_data["title"])
    tasks.append(new_task)
    save_tasks(tasks)
    task_id_counter += 1
    return {"id": new_task.id, "title": new_task.title, "status": new_task.status}


@app.put("/tasks/{task_id}")
async def update_task(task_id: int, task_data: dict):
    for task in tasks:
        if task.id == task_id:
            if "title" in task_data:
                task.title = task_data["title"]
            if "status" in task_data:
                task.status = task_data["status"]
            save_tasks(tasks)
            return {"id": task.id, "title": task.title, "status": task.status}
    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    global tasks
    original_tasks_count = len(tasks)
    tasks = [task for task in tasks if task.id != task_id]
    if len(tasks) == original_tasks_count:
        raise HTTPException(status_code=404, detail="Task not found")
    save_tasks(tasks)
    return {"message": "Task deleted"}
