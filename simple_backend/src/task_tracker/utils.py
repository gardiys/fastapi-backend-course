from models import MyTasks
from schemas import Stateless
from fastapi import HTTPException

state = Stateless()


def post(task_name):
    try:
        task = MyTasks(task_name=task_name)

        tasks = state.get_state()
        tasks.append(task.info)
        state.update_state(tasks)

        return task.info

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get():
    try:
        return state.get_state()
    except HTTPException as e:
        raise e


def put(task_id, name=None, status=None):
    try:
        tasks = state.get_state()

        for task in tasks:
            if task.get("id") == task_id:
                task["name"] = name or task.get("name")
                task["status"] = status or task.get("status")

                state.update_state(tasks)
                return task

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def delete(task_id: str):
    try:
        tasks = state.get_state()

        for task in tasks:
            if task.get("id") == task_id:
                tasks.remove(task)

                state.update_state(tasks)
                return task

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
