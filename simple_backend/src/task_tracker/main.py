from fastapi import FastAPI, Body
from json_db_lite import JSONDatabase

db_client = JSONDatabase("db.json")


app = FastAPI()


@app.get("/tasks")
def get_tasks() -> list | str:
    stat = db_client.get_all_records()
    if stat:
        return stat
    return "Tasks list is empty!"


@app.post("/tasks")
def create_task(text: str = Body(), status: bool = Body()) -> str:
    stat = db_client.get_all_records()
    if db_client:
        task_id = len(stat) + 1
    else:
        task_id = 1
    db_client.add_records({"id": task_id, "text": text, "status": status})
    return "Task created!"


@app.put("/tasks/{task_id}")
def update_task(task_id: int, text: str = Body(), status: bool = Body()) -> str:
    stat = db_client.get_all_records()
    if task_id <= len(stat):
        db_client.update_record_by_key(
            upd_filter={"id": task_id}, new_data=[{"text": text, "status": status}]
        )
        return "Task changed!"
    return f"Task ID{task_id} is not in task list!"


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int) -> str:
    stat = db_client.get_all_records()
    if task_id <= len(stat):
        db_client.delete_record_by_key(key="id", value=task_id)
        return f"Task ID{task_id} deleted!"
    return f"Task ID{task_id} is not in task list!"
