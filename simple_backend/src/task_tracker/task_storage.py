import requests
from fastapi import HTTPException
from pydantic import BaseModel
from typing import List


JSONBIN_API_KEY = "EOL870FGuEFEMaOsEiJhBOB2w3JhoxYt3sX6ZLKD3UcV4q0CgGnWy"
JSONBIN_BIN_ID = "67cc5b54ad19ca34f818af32"
JSONBIN_URL = f"https://api.jsonbin.io/v3/b/{JSONBIN_BIN_ID}"

HEADERS = {
    "X-Master-Key": JSONBIN_API_KEY,
    "Content-Type": "application/json"
}

# 🔹 Модель задачи
class Task(BaseModel):
    id: int
    title: str
    status: str

# 🔹 Класс для работы с JSONBin
class TaskStorage:
    def _load_tasks(self) -> List[dict]:
        """ Загружаем задачи из JSONBin """
        response = requests.get(JSONBIN_URL, headers=HEADERS)
        if response.status_code == 200:
            return response.json()["record"]["tasks"]
        else:
            return []

    def _save_tasks(self, tasks: List[dict]):
        """ Сохраняем задачи в JSONBin """
        data = {"tasks": tasks}
        response = requests.put(JSONBIN_URL, json=data, headers=HEADERS)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Ошибка сохранения в JSONBin")

    def get_tasks(self) -> List[dict]:
        return self._load_tasks()

    def add_task(self, task: Task):
        tasks = self._load_tasks()
        tasks.append(task.dict())
        print("Отправляю данные в jsonbin.io:", self.tasks)
        self._save_tasks(tasks)

    def update_task(self, task_id: int, updated_task: Task):
        tasks = self._load_tasks()
        for i, task in enumerate(tasks):
            if task["id"] == task_id:
                tasks[i] = updated_task.dict()
                self._save_tasks(tasks)
                return
        raise HTTPException(status_code=404, detail="Task not found")

    def delete_task(self, task_id: int):
        tasks = self._load_tasks()
        tasks = [task for task in tasks if task["id"] != task_id]
        self._save_tasks(tasks)
