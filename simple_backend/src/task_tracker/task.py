from enum import Enum
from typing import Optional, ClassVar
from pydantic import BaseModel, Field


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
    _next_id: ClassVar[int] = 1

    def __init__(self, **data):
        # Если ID не передан, генерируем автоматически
        if 'id' not in data:
            data['id'] = self.__class__._next_id
            self.__class__._next_id += 1
        super().__init__(**data)


class TaskUpdate(BaseModel):
    description: Optional[str] = Field(None, description="Описание задачи")
    status: Optional[TaskStatus] = Field(None, description="Статус задачи")
