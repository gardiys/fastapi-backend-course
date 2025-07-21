from pydantic import BaseModel

from const import TaskStatus

class Task(BaseModel):
    id: int
    title: str
    status: TaskStatus = TaskStatus.PLANNED

class TaskUpdate(BaseModel):
    title: str
    status: TaskStatus = TaskStatus.PLANNED