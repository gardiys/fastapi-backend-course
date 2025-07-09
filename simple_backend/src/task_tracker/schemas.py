# MARK: Schemas
from pydantic import BaseModel


class TaskCreateAndUpdateSchema(BaseModel):
    name: str
    status: str


class CreatedTaskReadSchema(BaseModel):
    id: int


class TaskReadSchema(TaskCreateAndUpdateSchema, CreatedTaskReadSchema):
    pass
