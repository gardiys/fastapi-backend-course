from enum import Enum
import uuid
from typing import Optional
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
    id: str
    solution_llm: Optional[str] = Field(None, description="Решение задачи от llm ассистента")

    def __init__(self, **data):
        # Если ID не передан, генерируем автоматически
        if 'id' not in data:
            data['id'] = str(uuid.uuid4())
        super().__init__(**data)


class TaskUpdate(BaseModel):
    description: Optional[str] = Field(None, description="Описание задачи")
    status: Optional[TaskStatus] = Field(None, description="Статус задачи")
