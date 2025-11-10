import json
from pathlib import Path
from models import Task
from basehttp import BaseHTTPClient

class IsMemoryStorage:

    def __init__(self):
        self.tasks = []
        self.next_task = 1


    def list_tasks(self) -> list:
        return self.tasks

    def create_task(self, task_data: dict) -> Task:
        task = Task(id=self.next_task, **task_data)
        self.tasks.append(task)
        self.next_task += 1

        return task

    def get_task(self, task_id)->Task:
        for task in self.tasks:
            if task['id'] == task_id:
                return task
        return None

    def update_task(self, task_id:int, task_data):
        for task in self.tasks:
            if task['id'] == task_id:
                task.update(task_data)
                return task
        return None


    def delete_task(self, task_id):
        task = self.get_task(task_id)
        if not task: return False
        self.tasks.remove(task)
        return True


class JSONStorage:
    def __init__(self, filepath: str | None = "tasks.json"):
        self.file = Path(filepath)
        if not self.file.exists():
            self.file.write_text("[]", encoding="utf-8")

    def _load(self) -> list[Task]:
        data = json.loads(self.file.read_text(encoding="utf-8"))
        return [Task(**t) for t in data]

    def _save(self, tasks: list[Task]):
        data = [t.model_dump() for t in tasks]
        self.file.write_text(json.dumps(data, indent=4, ensure_ascii=False), encoding="utf-8")

    def list_tasks(self) -> list[Task]:
        return self._load()

    def get_task(self, task_id: int) -> Task:
        for task in self._load():
            if task.id == task_id:
                return task
        raise ValueError(f"Task with id={task_id} not found")


    def create_task(self, task_data: Task) -> Task:
        tasks = self._load()
        new_id = max([t.id for t in tasks], default=0) + 1
        task = Task(id=new_id, **task_data.model_dump(exclude={'id'}))
        tasks.append(task)
        self._save(tasks)
        return task

    def update_task(self, task_id: int, task_data: Task) -> Task:
        tasks = self._load()
        task = next((t for t in tasks if t.id == task_id), None)
        if not task:
            raise ValueError(f"Task with id={task_id} not found")
        updated_task = task.model_copy(update=task_data.model_dump(exclude={'id'}))
        tasks[tasks.index(task)] = updated_task
        self._save(tasks)
        return updated_task

    def delete_task(self, task_id: int) -> Task:
        tasks = self._load()
        task = next((t for t in tasks if t.id == task_id), None)
        if not task:
            raise ValueError(f"Task with id={task_id} not found")
        tasks.remove(task)
        self._save(tasks)
        return task

class CloudJSONStorage(BaseHTTPClient, JSONStorage):
    def __init__(self, bin_id: str, master_key: str):
        super().__init__(
            base_url=f"https://api.jsonbin.io/v3/b/{bin_id}",
            headers={
                "X-Master-Key": master_key,
                "Content-Type": "application/json",
            }
        )

    def _load(self) -> list[Task]:
        record = self.get("latest").get("record", {})
        tasks_data = record.get("tasks", [])
        return [Task(**task) for task in tasks_data]

    def _save(self, tasks: list[Task]) -> dict:
        payload = {"tasks": [task.model_dump() for task in tasks]}
        return self.put("", json=payload)