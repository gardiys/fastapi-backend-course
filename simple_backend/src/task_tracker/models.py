from schemas import CloudFlare, Stateless
from pydantic import BaseModel, Field
from uuid import uuid4
from typing import Literal, Optional

state = Stateless()
llm = CloudFlare()


class MyTasks(BaseModel):
    task_id: str = Field(default_factory=lambda: uuid4().hex)
    task_name: str = Field(default="Новая задача")
    status: Literal["Открыта", "В работе", "Закрыта"] = Field(default="Открыта")
    solution: str = Field(default="Нет ответа")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.solution = llm.send_prompt(self.task_name)

    @property
    def solution_prop(self):
        return self.solution

    @solution_prop.setter
    def solution_prop(self, text):
        try:
            self.solution = text
        except Exception as e:
            print(e)

    @property
    def info(self):
        return {
            "id": self.task_id,
            "name": self.task_name,
            "status": self.status,
            "solution": self.solution,
        }

class TaskCreate(BaseModel):
    name: str = Field(..., description="Название задачи")


# Модель для обновления задачи (name и status)
class TaskUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Новое название задачи")
    status: Optional[Literal["Открыта", "В работе", "Закрыта"]] = Field(
        None, description="Новый статус задачи"
    )