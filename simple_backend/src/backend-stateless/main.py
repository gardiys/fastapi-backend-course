from fastapi import FastAPI, Body
import requests


class DataBase:
    __x_master_key = "$2a$10$IMh3f/dBpBNNOcK6OQMhJ.ZdcQWlXuR66nyHse7Jhto3MCUka62vm"

    def read(self):
        url = "https://api.jsonbin.io/v3/b/67ac93dfacd3cb34a8df05f9/latest"
        headers = {"X-Master-Key": self.__x_master_key, "X-Bin-Meta": "false"}

        response = requests.get(url, json=None, headers=headers)

        return response.json()

    def create(self, message: str, status: bool):
        stat = self.read()
        if stat:
            task_id = len(stat) + 1
        else:
            task_id = 1

        url = "https://api.jsonbin.io/v3/b"
        headers = {
            "Content-Type": "application/json",
            "X-Master-Key": self.__x_master_key,
        }
        data = {task_id: {"text": message, "status": status}}

        requests.post(url, json=data, headers=headers)

        return "To do list created!"

    def update(self, task_id: int, message: str, status: bool):
        stat = self.read()
        if task_id <= len(stat()):
            url = "https://api.jsonbin.io/v3/b/67ac93dfacd3cb34a8df05f9"
            headers = {
                "Content-Type": "application/json",
                "X-Master-Key": self.__x_master_key,
            }
            data = {task_id: {"text": message, "status": status}}
            requests.put(url, json=data, headers=headers)
            return "Task created!"
        return f"Task ID{task_id} is not in task list!"

    def delete(self):
        url = "https://api.jsonbin.io/v3/b/67ac93dfacd3cb34a8df05f9"
        headers = {
            "X-Master-Key": self.__x_master_key,
        }
        requests.delete(url, json=None, headers=headers)

        return "To do list delete!"


app = FastAPI()

db = DataBase()


@app.get("/tasks")
def get_tasks():
    result = db.read()
    return result


@app.post("/tasks")
def create_task(text: str = Body(), status: bool = Body()) -> str:
    result = db.create(text, status)
    return result


@app.put("/tasks/{task_id}")
def update_task(task_id: int, text: str = Body(), status: bool = Body()) -> str:
    result = db.update(task_id, text, status)
    return result


@app.delete("/tasks/{task_id}")
def delete_task() -> str:
    result = db.delete()
    return result
