from fastapi import FastAPI, Body
from json_db_lite import JSONDatabase


class DataBase:
    db_client = JSONDatabase("db.json")

    @property
    def get_task(self) -> str | list:
        stat = self.db_client.get_all_records()
        if stat:
            return stat
        return "Tasks list is empty!"

    def create_task(self, message: str, status: bool):
        stat = self.db_client.get_all_records()
        if stat:
            task_id = len(stat) + 1
        else:
            task_id = 1
        self.db_client.add_records({"id": task_id, "text": message, "status": status})
        return "Task created!"

    def update_task(self, task_id: int, message: str, status: bool):
        stat = self.db_client.get_all_records()
        if task_id <= len(stat):
            self.db_client.update_record_by_key(
                upd_filter={"id": task_id}, new_data=[{"text": message, "status": status}]
            )
            return "Task changed!"
        return f"Task ID{task_id} is not in task list!"

    def delete_task(self, task_id: int):
        stat = self.db_client.get_all_records()
        if task_id <= len(stat):
            self.db_client.delete_record_by_key(key="id", value=task_id)
            return f"Task ID{task_id} deleted!"
        return f"Task ID{task_id} is not in task list!"


app = FastAPI()

db = DataBase()


@app.get("/tasks")
def get_tasks() -> str | list:
    result = db.get_task
    return result


@app.post("/tasks")
def create_task(text: str = Body(), status: bool = Body()) -> str:
    result = db.create_task(text, status)
    return result


@app.put("/tasks/{task_id}")
def update_task(task_id: int, text: str = Body(), status: bool = Body()) -> str:
    result = db.update_task(task_id, text, status)
    return result


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int) -> str:
    result = db.delete_task(task_id)
    return result
