'''backend'''
from fastapi import FastAPI, HTTPException
from storage_gist import GistStorage
from Cloudflare import Cloudflare
app = FastAPI()
storage = GistStorage()
llm = Cloudflare()
# return tasks list
@app.get("/tasks")
def get_tasks():
    return storage.load()
#create a new task with id, name, and status 
@app.post("/tasks")
def create_task(name: str, condition: str = 'new'):
    tasks = storage.load()
    new_id = len(tasks) + 1
    llm_response = llm.get_llm_response(name)
    task = {'id': new_id, 'name': name, 'condition': condition, 'description': f'LLM Suggestion: {llm_response}'}
    tasks.append(task)
    storage.save(tasks)
    return task
#update task    
@app.put("/tasks/{task_id}")
def update_task(task_id: int, name: str, condition: str):
    tasks = storage.load()
    for task in tasks:
        if task['id'] == task_id:
            task['name'] = name
            task['condition'] = condition
            storage.save(tasks)
            return task
    raise HTTPException(status_code = 404, detail = 'task not found')
#delete task
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    tasks = storage.load()
    for task in tasks:
        if task['id'] == task_id:
            tasks.remove(task)
            storage.save(tasks)
            return 'task deleted'
    raise HTTPException(status_code = 404, detail = 'task not found') 