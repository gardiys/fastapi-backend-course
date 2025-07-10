from fastapi import FastAPI

import constants
import exceptions
import utils
from schemas import TaskCreateAndUpdateSchema, TaskSchema

app = FastAPI()

task_file_service = utils.JSONFileService(target_file_path=constants.TASKS_FILE_PATH)


@app.get("/tasks")
def get_tasks() -> list[TaskSchema]:
    return task_file_service.load_entities()


@app.post("/tasks")
def create_task(task: TaskCreateAndUpdateSchema) -> TaskSchema:
    tasks = task_file_service.load_entities()

    created_task = task.model_dump()
    created_task_id = tasks[-1]["id"] + 1 if tasks else 1
    created_task["id"] = created_task_id

    tasks.append(created_task)

    task_file_service.dump_entities(entities=tasks)

    return TaskSchema(**created_task)


@app.put("/tasks/{task_id}")
def update_task(task_id: int, update_data: TaskCreateAndUpdateSchema) -> TaskSchema:
    tasks = task_file_service.load_entities()

    for task in tasks:
        if task["id"] == task_id:
            task["name"] = update_data.name
            task["status"] = update_data.status

            task_file_service.dump_entities(entities=tasks)
            return TaskSchema(**task)

    else:
        raise exceptions.TaskNotFoundException


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int) -> None:
    tasks = task_file_service.load_entities()

    for i in range(len(tasks)):
        if tasks[i]["id"] == task_id:
            del tasks[i]
            task_file_service.dump_entities(entities=tasks)
            break

    else:
        raise exceptions.TaskNotFoundException
