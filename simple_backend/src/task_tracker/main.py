from fastapi import FastAPI
from pydantic import BaseModel
import json
from typing import List

app = FastAPI()

class Task(BaseModel):
    id: int
    title: str
    completed: bool = False

class TaskManager:
    def __init__(self, filename: str = 'tasks.json'):
        self.filename = filename
    
    def load_tasks(self) -> List[Task]:
        """Загрузить задачи из файла"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [Task(**task) for task in data]
        except (FileNotFoundError, json.JSONDecodeError):
            # Создаем начальные задачи если файл не существует или поврежден
            initial_tasks = [
                {"id": 1, "title": "купить молоко", "completed": False},
                {"id": 2, "title": "позавтракать", "completed": True},
                {"id": 3, "title": "позвонить дедушке", "completed": False}
            ]
            self._save_tasks_data(initial_tasks)
            return [Task(**task) for task in initial_tasks]
    
    def save_tasks(self, tasks: List[Task]) -> None:
        """Сохранить задачи в файл"""
        data = [task.model_dump() for task in tasks]
        self._save_tasks_data(data)
    
    def _save_tasks_data(self, data: list) -> None:
        """Внутренний метод для сохранения данных"""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def get_next_id(self, tasks: List[Task]) -> int:
        """Получить следующий ID для новой задачи"""
        if not tasks:
            return 1
        return max(task.id for task in tasks) + 1

# Создаем экземпляр менеджера задач
task_manager = TaskManager()

# GET /tasks - получить все задачи
@app.get("/tasks")
def get_tasks():
    return task_manager.load_tasks()

# POST /tasks - создать новую задачу
@app.post("/tasks")
def create_task(title: str):
    tasks = task_manager.load_tasks()
    new_id = task_manager.get_next_id(tasks)
    new_task = Task(id=new_id, title=title, completed=False)
    tasks.append(new_task)
    task_manager.save_tasks(tasks)
    return new_task

# PUT /tasks/{id} - обновить задачу
@app.put("/tasks/{task_id}")
def update_task(task_id: int, title: str = None, completed: bool = None):
    tasks = task_manager.load_tasks()
    for task in tasks:
        if task.id == task_id:
            if title is not None:
                task.title = title
            if completed is not None:
                task.completed = completed
            task_manager.save_tasks(tasks)
            return task
    return {"error": "Задача не найдена"}

# DELETE /tasks/{id} - удалить задачу
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    tasks = task_manager.load_tasks()
    for i, task in enumerate(tasks):
        if task.id == task_id:
            deleted_task = tasks.pop(i)
            task_manager.save_tasks(tasks)
            return {"message": f"Задача '{deleted_task.title}' удалена"}
    return {"error": "Задача не найдена"}