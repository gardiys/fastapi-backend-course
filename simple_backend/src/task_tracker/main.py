from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
from utils import get, post, put, delete

app = FastAPI()


@app.get("/tasks")
def get_tasks():
    tasks = get()
    if "error" in tasks:
        return JSONResponse(status_code=500, content={"message": tasks["error"]})
    return {"message": tasks}


@app.post("/tasks")
def create_task(data=Body()):
    if not data.get("name"):
        return JSONResponse(
            status_code=400, content={"message": "Неверный формат данных"}
        )

    task = post(data["name"])
    if "error" in task:
        return JSONResponse(status_code=500, content={"message": task["error"]})
    return {"message": "Задача добавлена", "response": task}


@app.put("/tasks/{task_id}")
def update_task(task_id: int, data=Body()):
    if not data.get("name") and not data.get("status"):
        return JSONResponse(
            status_code=400, content={"message": "Неверный формат данных"}
        )

    task = put(task_id, data.get("name"), data.get("status"))
    if "error" in task:
        return JSONResponse(status_code=500, content={"message": task["error"]})
    return {"message": "Задача была обновлена", "response": task}


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    task = delete(task_id)
    if "error" in task:
        return JSONResponse(status_code=500, content={"message": task["error"]})
    return {"message": "Задача была удалена", "response": task}
