import exceptions
from fastapi import FastAPI
from schemas import CreatedTaskReadSchema, TaskCreateAndUpdateSchema, TaskReadSchema

app = FastAPI()

tasks = list()


@app.get("/tasks")
def get_tasks() -> list[TaskReadSchema]:
    return tasks


@app.post("/tasks")
def create_task(task: TaskCreateAndUpdateSchema) -> CreatedTaskReadSchema:
    created_task_id = tasks[-1].id + 1 if tasks else 1

    tasks.append(TaskReadSchema(**task.model_dump(), id=created_task_id))

    return CreatedTaskReadSchema(id=created_task_id)


@app.put("/tasks/{task_id}")
def update_task(task_id: int, update_data: TaskCreateAndUpdateSchema) -> None:
    for task in tasks:
        if task.id == task_id:
            task.name = update_data.name
            task.status = update_data.status
            break
    else:
        raise exceptions.TaskNotFoundException


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int) -> None:
    for i in range(len(tasks)):
        if tasks[i].id == task_id:
            del tasks[i]
            break
    else:
        raise exceptions.TaskNotFoundException
