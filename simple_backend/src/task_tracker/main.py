from fastapi import FastAPI, HTTPException
from classes import RemoteTaskStorage, CloudflareAIClient

app = FastAPI()

STATUS_LIST = ["Задача создана", "Задача в процессе выполнения", "Задача выполнена"]
DEFAULT_STATUS = STATUS_LIST[0]

storage = RemoteTaskStorage()
ai = CloudflareAIClient()

def next_id() -> int:
    tasks = storage.load()
    return max((t["task_id"] for t in tasks), default=0) + 1

class Task:
    def __init__(self, name: str):
        self.task_id = next_id()
        self.name = name
        self.status = DEFAULT_STATUS
    def to_dict(self):
        return {"task_id": self.task_id, "name": self.name, "status": self.status}

@app.get("/tasks")
def get_tasks() -> list[dict]:
    return storage.load()

@app.post("/tasks")
def create_task(name: str):
    tasks = storage.load()
    try:
        tip = ai.explain(f"Объясни пошагово, как решать вот эту задачу -> {name} ")
        full_name = f"{name} \n\nПодсказка LLM:\n{tip}"
    except Exception:
        full_name = name
    new_task = Task(full_name)
    tasks.append(new_task.to_dict())
    storage.save(tasks)
    return new_task.to_dict()

@app.put("/tasks/{task_id}")
def update_task(task_id: int):
    tasks = storage.load()
    for t in tasks:
        if t["task_id"] == task_id:
            if t["status"] == DEFAULT_STATUS:
                t["status"] = STATUS_LIST[1]
            elif t["status"] == STATUS_LIST[1]:
                t["status"] = STATUS_LIST[2]
            storage.save(tasks)
            return t
    raise HTTPException(404, "ID не найден")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    tasks = storage.load()
    for i, t in enumerate(tasks):
        if t["task_id"] == task_id:
            tasks.pop(i)
            storage.save(tasks)
            return {"detail": "Удалено"}
    raise HTTPException(404, "ID не найден")