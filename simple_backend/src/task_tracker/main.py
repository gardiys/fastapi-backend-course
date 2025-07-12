from fastapi import FastAPI

import exceptions
from config import settings
from schemas import TaskCreateSchema, TaskSchema, TaskUpdateSchema
from utils.cloudflare_utils import CloudflareService
from utils.jsonbin_utils import JSONBinService

app = FastAPI()

jsonbin_service = JSONBinService(
    bin_id=settings.JSONBIN_BIN_ID,
    access_key=settings.JSONBIN_ACCESS_KEY,
    master_key=settings.JSONBIN_MASTER_KEY,
)
cloudflare_service = CloudflareService(
    account_id=settings.CLOUDFLARE_ACCOUNT_ID, api_token=settings.CLOUDFLARE_API_TOKEN
)


@app.get("/tasks")
async def get_tasks() -> list[TaskSchema]:
    return await jsonbin_service.load_entities()


@app.post("/tasks")
async def create_task(task: TaskCreateSchema) -> TaskSchema:
    solution = await cloudflare_service.get_solution(task_description=task.description)
    tasks = await jsonbin_service.load_entities()

    created_task = task.model_dump()
    created_task_id = tasks[-1]["id"] + 1 if tasks else 1
    created_task["id"] = created_task_id
    created_task["solution"] = solution

    tasks.append(created_task)
    await jsonbin_service.dump_entities(entities=tasks)

    return TaskSchema(**created_task)


@app.put("/tasks/{task_id}")
async def update_task(task_id: int, update_data: TaskUpdateSchema) -> TaskSchema:
    tasks = await jsonbin_service.load_entities()

    for task in tasks:
        if task["id"] == task_id:
            task.update(update_data)
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
