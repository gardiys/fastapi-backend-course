from db import DataBase
from models import MyTasks


db = DataBase("database.json")


def post(task_name):
    task = MyTasks(task_name)

    if not (tasks := db.get_data()):
        tasks = []

    tasks.append(task.info)

    if db.save_changes(tasks):
        return task.info

    return None


def get():
    if not (tasks := db.get_data()):
        return None

    return tasks


def put(task_id, name=None, status=None):
    if not (tasks := db.get_data()):
        return None

    for task in tasks:
        if task.get("id") == task_id:
            task["name"] = name or task.get("name")
            task["status"] = status or task.get("status")

            if db.save_changes(tasks):
                return task

            return task

    return None


def delete(task_id: int):
    if not (tasks := db.get_data()):
        return None

    for task in tasks:
        if task.get("id") == task_id:
            poped_task = tasks.pop(task_id - 1)

            if db.save_changes(tasks):
                return poped_task

    return None
