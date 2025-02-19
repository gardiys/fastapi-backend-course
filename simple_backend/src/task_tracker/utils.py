from models import MyTasks


def post(task_name):
    task = MyTasks(task_name)
    MyTasks.all_tasks.append(task)
    return {"id": task.task_id, "name": task.task_name, "status": task.status}


def get():
    if MyTasks.all_tasks:
        return [
            {"id": task.task_id, "name": task.task_name, "status": task.status}
            for task in MyTasks.all_tasks
        ]


def put(task_id, name=None, status=None):
    if not MyTasks.all_tasks:
        return None

    for task in MyTasks.all_tasks:
        if task.task_id == task_id:
            task.task_name = name or task.task_name
            task.status = status or task.status
            return {"id": task.task_id, "name": task.task_name, "status": task.status}


def delete(task_id: int):
    if not MyTasks.all_tasks:
        return None

    for task in MyTasks.all_tasks:
        if task.task_id == task_id:
            poped_task = MyTasks.all_tasks.pop(task_id - 1)
            return {
                "id": poped_task.task_id,
                "name": poped_task.task_name,
                "status": poped_task.status,
            }
