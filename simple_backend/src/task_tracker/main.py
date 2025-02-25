from fastapi import FastAPI

app = FastAPI()

tasks = []

@app.get("/tasks")
def get_tasks():
    return tasks

@app.post("/tasks")
def create_task(id, name, status):
    a = []
    a.append(id)
    a.append(name)
    a.append(status)
    tasks.append(a)
    return 'Task created'

@app.put("/tasks/{task_id}")
def update_task(task_id: int):
    tasks[task_id] = 'Updated'
    return 'Task updated'

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    del tasks[task_id]
    return 'Task deleted'
