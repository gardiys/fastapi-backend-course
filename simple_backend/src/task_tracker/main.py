from fastapi import FastAPI, Body, status
from fastapi.responses import JSONResponse
from utils import get, post, put, delete

app = FastAPI()


@app.get("/tasks")
def get_tasks():
    if response := get():
        return {"message": response}

    return JSONResponse(status_code=200, content={"message": "Список пуст"})


@app.post("/tasks")
def create_task(data=Body()):
    if not data.get("name"):
        return JSONResponse(
            status_code=400, content={"message": "Неверный формат данных"}
        )

    if response := post(data["name"]):
        return {"message": "Задача добавлена", "response": response}

    return JSONResponse(
        status_code=500, content={"message": "Не получилось добавить задачу"}
    )


@app.put("/tasks/{task_id}")
def update_task(task_id: int, data=Body()):
    if not data.get("name") and not data.get("status"):
        return JSONResponse(
            status_code=400, content={"message": "Неверный формат данных"}
        )

    if response := put(task_id, data.get("name"), data.get("status")):
        return {"message": "Задача была обновлена", "response": response}

    return JSONResponse(
        status_code=500, content={"message": "Не получилось обновить задачу"}
    )


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    if response := delete(task_id):
        return ({"message": "Задача была удалена", "response": response},)

    return JSONResponse(
        status_code=500, content={"message": "Не получилось удалить задачу"}
    )
