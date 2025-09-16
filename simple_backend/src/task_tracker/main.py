from fastapi import FastAPI, Query

app = FastAPI()

tasks = []

@app.get("/tasks")
def get_tasks():
    return tasks

@app.post("/tasks")
def create_task(
    task: str = Query(...),
    status: str = Query(...)
):
    if isinstance(status, str) and isinstance(task, str):
        task_status = status
        task_name = task
        task_id = len(tasks) + 1
        new_task = {'id': task_id, 'name': task_name, 'status': task_status}
        tasks.append(new_task)
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
        for i in tasks:
            if i['id'] == task_id:
                i['name'] = new_name
                i['status'] = new_status
                return i
    else:
        raise ValueError('name and status only str and id only int')
    

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    if isinstance(task_id, int):
        for i in tasks:
            if i['id'] == task_id:
                tasks.remove(i)
                return {"message": "Task deleted"}
    else:
        raise ValueError('task_id only int')