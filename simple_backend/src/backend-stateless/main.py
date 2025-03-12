from fastapi import FastAPI, Body
import requests

from config import Configs


class DataBase:
    __x_master_key = Configs.get_secret
    __url = "https://api.jsonbin.io/v3/b/67ac93dfacd3cb34a8df05f9"
    __headers = {
        "Content-Type": "application/json",
        "X-Master-Key": __x_master_key,
    }

    @property
    def url(self):
        return self.__url

    @property
    def headers(self):
        return self.__headers

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

        stat[task_id] = {"text": message, "status": status}
        requests.put(url=self.url, json=stat, headers=self.headers)
        return "Task created!"

    def update(self, task_id: str, message: str, status: bool):
        stat = self.read()
        if task_id in stat.keys():
            stat[task_id] = {"text": message, "status": status}
            requests.put(url=self.url, json=stat, headers=self.headers)
            return "Task update!"
        return f"Task ID{task_id} is not in task list!"

    def delete(self, task_id: str):
        stat = self.read()
        if task_id in stat.keys():
            stat.pop(task_id)
            requests.put(url=self.url, json=stat, headers=self.headers)
            return "Task delete!"
        return f"Task ID{task_id} is not in task list!"


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
def update_task(task_id: str, text: str = Body(), status: bool = Body()) -> str:
    result = db.update(task_id, text, status)
    return result


@app.delete("/tasks/{task_id}")
def delete_task(task_id: str) -> str:
    result = db.delete(task_id)
    return result
