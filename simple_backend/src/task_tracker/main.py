from fastapi import FastAPI, HTTPException, status
from typing import List

from cloud_storage import MockApiTasks, MockApiConfig, Task, TaskUpdate
from llm_assistant import LLMAssistant

app = FastAPI()

MOCKAPI_API_URL = "https://68aa779b909a5835049c516f.mockapi.io/"
MOCKAPI_RESOURCE = "tasks"

llm = LLMAssistant(api_token="API_TOKEN", account_id="ACCOUNT_ID")

tasks_db = MockApiTasks(MockApiConfig(api_url=MOCKAPI_API_URL, resource=MOCKAPI_RESOURCE))


@app.get("/tasks", response_model=List[Task])
def get_tasks() -> List[Task]:
    return tasks_db.get_all()


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task: Task) -> Task:
    answer = llm.task_llm(task.title)
    if answer:
        task.title = f"{task.title}\n\nРешение от AI: {answer}"
    else:
        task.title = f"{task.title}\n\Не удалось получить решение от AI"
    return tasks_db.add(task)


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: str, task_update: TaskUpdate) -> Task:
    try:
        return tasks_db.update(task_id, task_update)
    except KeyError:
        raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str) -> None:
    try:
        tasks_db.delete(task_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Task not found")
