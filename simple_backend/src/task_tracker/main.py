from fastapi import FastAPI

app = FastAPI()

class Task:
    def __init__(self, task_id: int, title: str, status: str = "in work"):
        self.task_id = task_id
        self.title = title
        self.status = status
    def to_dict(self):
        return {"id" : self.task_id, "title" : self.title, "status" : self.status}

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.next_id = 1

    def get_all_tasks(self):
        return [task.to_dict() for task in self.tasks]

    def create_task(self, title: str):
        task = Task(self.next_id, title, status="in work")
        self.tasks.append(task)
        self.next_id += 1
        return task.to_dict()

    def update_task(self, task_id: int, title: str = None, status: str = None):
        for task in self.tasks:
            if task.task_id == task_id:
                if title:
                    task.title = title
                if status:
                    task.status = status
                return task.to_dict()
        raise Exception("Task not found")
    def delete_task(self, task_id: int):
        for task in self.tasks:
            if task.task_id == task_id:
                self.tasks.remove(task)
                return {"message": "Task deleted"}
        raise Exception("Task not found")

task_manager = TaskManager()

@app.get("/tasks")
def get_tasks():
    return task_manager.get_all_tasks()

@app.post("/tasks")
def create_task(title: str):
    return task_manager.create_task(title)

@app.put("/tasks/{task_id}")
def update_task(task_id: int, title: str = None, status: str = None):
    return task_manager.update_task(task_id, title, status)

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    return task_manager.delete_task(task_id)

