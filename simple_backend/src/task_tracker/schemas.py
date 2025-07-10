# MARK: Schemas
from pydantic import BaseModel


class TaskCreateAndUpdateSchema(BaseModel):
    name: str
    status: str


class TaskSchema(TaskCreateAndUpdateSchema):
    id: int
