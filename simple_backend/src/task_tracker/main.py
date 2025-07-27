from fastapi import FastAPI,HTTPException
from typing import List
from model import Task
from task_tracker import Tack_tracker

app = FastAPI()



FILE_PATH = "tasks.json"
task_tracker = Tack_tracker(FILE_PATH)



@app.get("/tasks",response_model=List[Task])
def get_tasks():
    json_data = task_tracker.load_json()
    return task_tracker.json_to_task(json_data)

@app.post("/tasks")
def create_task(task:Task):

    json_data = task_tracker.load_json()
    json_data.append(task.dict())
    task_tracker.save_json(json_data)
    return task

@app.put("/tasks/{task_id}",response_model=Task)
def update_task(task_id: int,updated_task:Task):
    json_data = task_tracker.load_json()
    tasks = task_tracker.json_to_task(json_data)
    for index in range(len(tasks)):
        if tasks[index].id == task_id:
            tasks[index] = updated_task
            task_tracker.save_json(task_tracker.task_to_json(tasks))
            return updated_task
    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    json_data = task_tracker.load_json()
    tasks = task_tracker.json_to_task(json_data)
    for index in range(len(tasks)):
        if tasks[index].id == task_id:
            task_del = tasks.pop(index)
            task_tracker.save_json(task_tracker.task_to_json(tasks))
            return task_del
    raise HTTPException(status_code=404,detail="Task not found")

