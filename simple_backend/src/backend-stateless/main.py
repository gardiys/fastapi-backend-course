from fastapi import FastAPI, Body
import requests

from simple_backend.src.task_tracker.backend.config import Configs


class DataBase:
    base_url = "https://api.jsonbin.io/v3/b/"
    headers = {
        "Content-Type": "application/json",
        "X-Master-Key": Configs.get_secret,
    }

    headers_for_read = {
        "X-Master-Key": Configs.get_secret,
        "X-Bin-Meta": "false"
    }

    def __init__(self, url_id: str):
        self.url = f'{self.base_url}{url_id}'

    def read(self):
        try:
            response = requests.get(url=f'{self.url}/latest', json=None, headers=self.headers_for_read)

            return response.json()

        except requests.exceptions.HTTPError as http_err:
            return {
                "success": False,
                "error": str(http_err)
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def create(self, message: str, status: bool):
        try:
            stat = self.read()
            if stat:
                task_id = len(stat) + 1
            else:
                task_id = 1

            stat[task_id] = {"text": message, "status": status}
            requests.put(url=self.url, json=stat, headers=self.headers)
            return {
                "success": True,
                "data": {
                    "id": task_id,
                    "text": message,
                    "status": status
                }
            }

        except requests.exceptions.HTTPError as http_err:
            return {
                "success": False,
                "error": str(http_err)
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def update(self, task_id: str, message: str, status: bool):
        try:
            stat = self.read()
            if task_id in stat.keys():
                stat[task_id] = {"text": message, "status": status}
                requests.put(url=self.url, json=stat, headers=self.headers)
            return {
                "success": True,
                "new_data": {
                    "id": task_id,
                    "text": message,
                    "status": status
                }
            }

        except requests.exceptions.HTTPError as http_err:
            return {
                "success": False,
                "error": str(http_err)
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def delete(self, task_id: str):
        try:
            stat = self.read()
            if task_id in stat.keys():
                stat.pop(task_id)
                requests.put(url=self.url, json=stat, headers=self.headers)
            return {"success": True}

        except requests.exceptions.HTTPError as http_err:
            return {
                "success": False,
                "error": str(http_err)
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


app = FastAPI()

db = DataBase(url_id='67ac93dfacd3cb34a8df05f9')


@app.get("/tasks")
def get_tasks():
    result = db.read()
    return result


@app.post("/tasks")
def create_task(text: str = Body(), status: bool = Body()) -> dict:
    result = db.create(text, status)
    return result


@app.put("/tasks/{task_id}")
def update_task(task_id: str, text: str = Body(), status: bool = Body()) -> dict:
    result = db.update(task_id, text, status)
    return result


@app.delete("/tasks/{task_id}")
def delete_task(task_id: str) -> dict:
    result = db.delete(task_id)
    return result
