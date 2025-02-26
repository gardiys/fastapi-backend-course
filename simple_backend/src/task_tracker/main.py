from fastapi import FastAPI

app = FastAPI()

class Task():
    id: int
    name: str
    status: str

tasks = [
    Task(id=1, name='Sample Task', status='Open')
]

@app.get("/tasks")
def get_tasks():
    return tasks

@app.post("/tasks")
def create_task(task: Task):
    new_task = Task(id=task.id, name=task.name, status=task.status)
    tasks.append(new_task)
    return new_task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    for i, t in enumerate(tasks):
        if t.id == task_id:
            tasks[i] = Task(id=task.id, name=task.name, status=task.status)
            return tasks[i]

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    global tasks
    tasks = [t for t in tasks if t.id != task_id]
    return