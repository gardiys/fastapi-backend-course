from pydantic import BaseModel, ConfigDict
from const import TaskStatus

class Task(BaseModel):
    id: int
    title: str
    status: TaskStatus = TaskStatus.PLANNED

    model_config = ConfigDict(use_enum_values=True)