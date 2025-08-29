from enum import Enum
from typing import Optional, Annotated
from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field

app = FastAPI()

tasks = []
tasks_id = 0


class TaskStatus(str, Enum):
    NOT_STARTED = "Не выполнено"
    IN_PROGRESS = "В процессе"
    COMPLETED = "Выполнено"


class TaskAdd(BaseModel):
    name: str = Field()
    description: Optional[str] = Field(None, description="Описание задачи")
    status: Optional[TaskStatus] = Field(TaskStatus.NOT_STARTED, description="Статус задачи")


class Task(TaskAdd):
    id: int


class TaskUpdate(BaseModel):
    # id: int = Field(json_schema_extra={"readOnly": True})
    # name: str = Field(json_schema_extra={"readOnly": True}, exclude=True)
    description: Optional[str] = Field(None, description="Описание задачи")
    status: Optional[TaskStatus] = Field(None, description="Статус задачи")


@app.get("/tasks")
def get_tasks():
    return tasks


@app.post("/tasks")
def create_task(task: Annotated[TaskAdd, Depends()]):
    global tasks_id
    tasks_id += 1
    obj = Task(id=tasks_id, **task.dict())
    tasks.append(obj)
    return f'Ok'


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Annotated[TaskUpdate, Depends()]):
    for obj in tasks:
        if task_id != obj.id:
            continue
        obj.description = task.description if task.description else obj.description
        obj.status = task.status if task.status else obj.status
        return 'ok'
    raise KeyError("Задача с таким id несуществует")


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for obj in tasks:
        if task_id != obj.id:
            continue
        tasks.remove(obj)
        return 'ok'
    raise KeyError("Задача с таким id несуществует")
