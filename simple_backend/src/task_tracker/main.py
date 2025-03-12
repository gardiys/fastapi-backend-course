from fastapi import FastAPI, Body
from json_db_lite import JSONDatabase


class DataBase:
    def __init__(self, db_client):
        self.db_client = db_client

    @property
    def get_task(self) -> str | list:
        stat = self.db_client.get_all_records()
        if stat:
            return stat
        return "Tasks list is empty!"

    def create_task(self, message: str, status: bool):
        try:
            stat = self.db_client.get_all_records()
            if stat:
                task_id = len(stat) + 1
            else:
                task_id = 1
            self.db_client.add_records({"id": task_id, "text": message, "status": status})
            return {
                "success": True,
                "data": {
                    "id": task_id,
                    "text": message,
                    "status": status
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def update_task(self, task_id: int, message: str, status: bool):
        try:
            stat = self.db_client.get_all_records()
            if task_id <= len(stat):
                self.db_client.update_record_by_key(
                    upd_filter={"id": task_id},
                    new_data=[{"text": message, "status": status}],
                )
                return {
                    "success": True,
                    "new_data": {
                        "id": task_id,
                        "text": message,
                        "status": status
                    }
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def delete_task(self, task_id: int):
        try:
            stat = self.db_client.get_all_records()
            if task_id <= len(stat):
                self.db_client.delete_record_by_key(key="id", value=task_id)
                return {"status": True}
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


app = FastAPI()

db = DataBase(JSONDatabase("db.json"))


@app.get("/tasks")
def get_tasks() -> str | list:
    result = db.get_task
    return result


@app.post("/tasks")
def create_task(text: str = Body(), status: bool = Body()) -> dict:
    result = db.create_task(text, status)
    return result


@app.put("/tasks/{task_id}")
def update_task(task_id: int, text: str = Body(), status: bool = Body()) -> dict:
    result = db.update_task(task_id, text, status)
    return result


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int) -> dict:
    result = db.delete_task(task_id)
    return result
