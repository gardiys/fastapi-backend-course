# MARK: Schemas
from pydantic import BaseModel


class TaskCreateSchema(BaseModel):
    name: str
    status: str
    description: str


class TaskUpdateSchema(TaskCreateSchema):
    solution: str


class TaskSchema(TaskUpdateSchema):
    id: int
