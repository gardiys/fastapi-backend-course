from models import MyTasks
from schemas import Stateless


state = Stateless()


def post(task_name):
    task = MyTasks(task_name)

    tasks = state.get_state()
    if "error" in tasks:
        return tasks

    tasks.append(task.info)

    if state.update_state(tasks):
        return task.info
    else:
        return {"error": "Не удалось обновить состояние"}


def get():
    tasks = state.get_state()
    return tasks


def put(task_id, name=None, status=None):
    tasks = state.get_state()
    if "error" in tasks:
        return tasks

    for task in tasks:
        if task.get("id") == task_id:
            task["name"] = name or task.get("name")
            task["status"] = status or task.get("status")

            if state.update_state(tasks):
                return task

            return {"error": "Не удалось обновить состояние"}

    return {"error": "Задача не найдена"}


def delete(task_id: int):
    tasks = state.get_state()
    if "error" in tasks:
        return tasks

    for task in tasks:
        if task.get("id") == task_id:
            tasks.remove(task)

            if state.update_state(tasks):
                return task

            return {"error": "Не удалось обновить состояние"}

    return {"error": "Задача не найдена"}
