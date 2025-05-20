from fastapi import FastAPI , status

app = FastAPI()

task_user = {}

@app.get("/tasks")
def get_tasks() -> dict:
    return task_user

@app.post("/tasks",status_code=status.HTTP_201_CREATED)
def create_task(id:int,task_name,status_task):
    task_user[id] = [task_name,status_task]
    return f'Task created'

@app.put("/tasks/{task_id}")
def update_task(task_id: int,task_name, status_task):
    task_user[task_id] = [task_name,status_task]

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    task_user.pop(task_id)
