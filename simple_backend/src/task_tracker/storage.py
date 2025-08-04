import json
from pathlib import Path
from task_tracker.models import Task

TASKS_PATH = Path(__file__).parent / "tasks.json"

class TaskStorage:
    def get_tasks(self) -> list[Task]:
        if not TASKS_PATH.exists():
            return []
        with open(TASKS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [Task(**task) for task in data]

    def save_tasks(self, tasks: list[Task]):
        with open(TASKS_PATH, "w", encoding="utf-8") as f:
            json.dump([task.dict() for task in tasks], f, ensure_ascii=False, indent=2)

    def create_task(self, task: Task) -> Task:
        tasks = self.get_tasks()
        next_id = max((t.id for t in tasks), default=0) + 1
        task.id = next_id
        tasks.append(task)
        self.save_tasks(tasks)
        return task
