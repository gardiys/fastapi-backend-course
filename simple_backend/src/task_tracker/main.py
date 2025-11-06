from fastapi import FastAPI, HTTPException
from task_manager import TaskManager, TaskModel, TaskUpdateModel, TaskResponse
from typing import List

app = FastAPI()
task_manager = TaskManager()

@app.get('/tasks', response_model=List[TaskResponse])
def get_tasks():
    return task_manager.get_all()

@app.post('/tasks', response_model=TaskResponse)
def create_task(task: TaskModel):
    try:
        task_data = task.model_dump()
        return task_manager.create(
            title=task_data.get('title', ''),
            description=task_data.get('description', ''),
            status=task_data.get('status', False)
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: str, task_update: TaskUpdateModel):
    update_data = task_update.model_dump(exclude_unset=True)
    update = task_manager.update(task_id, **update_data)
    if not update:
        raise HTTPException(status_code=404, detail='Task not found')
    return update

@app.delete('/tasks/{task_id}')
def delete_task(task_id: str):
    result = task_manager.delete(task_id)
    if not result:
        raise HTTPException(status_code=404, detail='Task not found')
    return {'message': 'Task deleted'}