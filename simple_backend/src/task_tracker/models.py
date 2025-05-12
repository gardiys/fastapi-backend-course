from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional

# Допустимые статусы задачи
class StatusEnum(str, Enum):
    todo = "todo"
    in_progress = "in progress"
    done = "done"
    new = "новая"
    new2 = "обновочка"
    
#Модель для создания задачи(входные данные)
class CreateTask(BaseModel):
    description: str = Field(min_length=1,max_length=10000000)
    status: StatusEnum
    
#Модель для полной задачи(выходные данные)
class Task(CreateTask):
    id: int
    solution: Optional[str] = None
    
#Модель для обновления задачи
class UpdateTask(BaseModel):
    description: Optional[str] = Field(None, min_length=1, max_length=10000000)
    status: Optional[StatusEnum]
    
#Модель для входа
class UserLogin(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    password: str = Field(min_length=3, max_length=20)