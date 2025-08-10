from pydantic import BaseModel

class Task(BaseModel):
    id: int | None = None
    title: str
    status: str
