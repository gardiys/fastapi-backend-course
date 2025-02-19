from models import MyTasks
import json
import os


filename = "database.json"


def post(task_name):
    task = MyTasks(task_name)

    if not (tasks := read_database()):
        tasks = []

    tasks.append(task.info)

    if save_changes(tasks):
        return task.info

    return None


def get():
    if not (tasks := read_database()):
        return None

    return tasks


def put(task_id, name=None, status=None):
    if not (tasks := read_database()):
        return None

    for task in tasks:
        if task.get("id") == task_id:
            task["name"] = name or task.get("name")
            task["status"] = status or task.get("status")

            if save_changes(tasks):
                return task

            return task

    return None


def delete(task_id: int):
    if not (tasks := read_database()):
        return None

    for task in tasks:
        if task.get("id") == task_id:
            poped_task = tasks.pop(task_id - 1)

            if save_changes(tasks):
                return poped_task

    return None


def read_database():
    try:
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as file:
                tasks = json.load(file)
                return tasks
    except Exception as e:
        print(e)
        return None


def save_changes(data):
    try:
        if os.path.exists(filename):
            with open(filename, 'w', encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

        return True
    except Exception as e:
        print(e)
        return False