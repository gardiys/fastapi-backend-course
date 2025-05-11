from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional

# Допустимые статусы задачи
class StatusEnum(str, Enum):
    todo = "todo"
    in_progress = "in progress"
    done = "done"

#Модель для создания задачи(входные данные)
class CreateTask(BaseModel):
    title: str = Field(min_length=1,max_length=20)
    status: StatusEnum
    
#Модель для полной задачи(выходные данные)
class Task(CreateTask):
    id: int
    
#Модель для обновления задачи
class UpdateTask(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=20)
    status: Optional[StatusEnum]
    
#Модель для входа
class UserLogin(BaseModel):
    username: str
    password: str