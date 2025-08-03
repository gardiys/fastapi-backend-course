from pydantic import BaseModel


class Task(BaseModel):
    id: int
    title: str
    status: str
