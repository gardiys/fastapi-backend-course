from fastapi import FastAPI, HTTPException

app = FastAPI()

tasks = []
task_id_counter = 1


class Task:
    def __init__(self, id, title, status="To Do"):
        self.id = id
        self.title = title
        self.status = status


@app.get("/tasks")
async def get_tasks():
    task_list = []
    for task in tasks:
        task_list.append({"id": task.id, "title": task.title, "status": task.status})
    return task_list


@app.post("/tasks")
async def create_task(task_data: dict):
    global task_id_counter
    new_task = Task(id=task_id_counter, title=task_data["title"])
    tasks.append(new_task)
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
            return {"id": task.id, "title": task.title, "status": task.status}
    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    global tasks
    original_tasks_count = len(tasks)
    tasks = [task for task in tasks if task.id != task_id]
    if len(tasks) == original_tasks_count:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted"}
