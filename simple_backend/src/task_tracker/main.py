from fastapi import FastAPI

import exceptions
import jsonbin_utils
from config import settings
from schemas import TaskCreateAndUpdateSchema, TaskSchema

app = FastAPI()

jsonbin_service = jsonbin_utils.JSONBinService(
    bin_id=settings.JSONBIN_BIN_ID,
    access_key=settings.JSONBIN_ACCESS_KEY,
    master_key=settings.JSONBIN_MASTER_KEY,
)


@app.get("/tasks")
async def get_tasks() -> list[TaskSchema]:
    return await jsonbin_service.load_entities()


@app.post("/tasks")
async def create_task(task: TaskCreateAndUpdateSchema) -> TaskSchema:
    tasks = await jsonbin_service.load_entities()

    created_task = task.model_dump()
    created_task_id = tasks[-1]["id"] + 1 if tasks else 1
    created_task["id"] = created_task_id

    tasks.append(created_task)

    await jsonbin_service.dump_entities(entities=tasks)

    return TaskSchema(**created_task)


@app.put("/tasks/{task_id}")
async def update_task(
    task_id: int, update_data: TaskCreateAndUpdateSchema
) -> TaskSchema:
    tasks = await jsonbin_service.load_entities()

    for task in tasks:
        if task["id"] == task_id:
            task["name"] = update_data.name
            task["status"] = update_data.status

            await jsonbin_service.dump_entities(entities=tasks)
            return TaskSchema(**task)

    else:
        raise exceptions.TaskNotFound


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int) -> None:
    tasks = await jsonbin_service.load_entities()

    for i in range(len(tasks)):
        if tasks[i]["id"] == task_id:
            del tasks[i]
            await jsonbin_service.dump_entities(entities=tasks)
            break

    else:
        raise exceptions.TaskNotFound
