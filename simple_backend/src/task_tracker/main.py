from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from gist_storage import GistStorage
from cloudflare import CloudflareAI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

storage = GistStorage()
ai_client = CloudflareAI()

class CreateTask(BaseModel):
    task: str
    status: str = 'No'
    
class UpdateTask(BaseModel):
    task: str
    status: str

@app.get("/tasks", tags=['Вывод всех задач'])
def get_tasks():
    return storage.load_tasks()

@app.post("/tasks", tags=['Добавление задачи'])
def create_task(new_task: CreateTask):
    tasks = storage.load_tasks()
    max_id = max(task['id'] for task in tasks) + 1 if tasks else 1
    
    ai_advice = ai_client.get_advice(new_task.task)
    enhanced_task = f"{new_task.task}\n\nСоветы по решению:\n{ai_advice}"
    
    tasks.append({
        'id': max_id, 
        'task': enhanced_task,
        'status': new_task.status
    })
    
    storage.save_tasks(tasks)
    return {"success": True}

@app.put("/tasks/{task_id}", tags=['Обновление задачи'])
def update_task(task_id: int, update_task: UpdateTask):
    tasks = storage.load_tasks()
    for i in tasks:
        if i['id'] == task_id:
            i['task'] = update_task.task
            i['status'] = update_task.status
            storage.save_tasks(tasks)
            return {"success": True}
     
    raise HTTPException(status_code=404, detail='Задача не найдена')

@app.delete("/tasks/{task_id}", tags=['Удаление задачи'])
def delete_task(task_id: int):
    tasks = storage.load_tasks()
    for i, task in enumerate(tasks):
        if task['id'] == task_id:
            tasks.pop(i)
            storage.save_tasks(tasks)
            return {"success": True}     
        
    raise HTTPException(status_code=404, detail='Задача не найдена')