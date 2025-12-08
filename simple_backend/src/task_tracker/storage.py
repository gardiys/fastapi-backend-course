import json

class TaskFileStorage:
    def __init__(self, file_path: str):
        self.file_path = file_path

        try:
            open(self.file_path, "r").close()
        except FileNotFoundError:
            with open(self.file_path, "w") as f:
                json.dump([], f)

    def get_tasks(self):
        with open(self.file_path, "r") as f:
            return json.load(f)

    def create_task(self, task):
        tasks = self.get_tasks()
        tasks.append(task)

        with open(self.file_path, "w") as f:
            json.dump(tasks, f, indent=2)
        return task

    def update_task(self, task_id, updated_task):
        tasks = self.get_tasks()
        for i, task in enumerate(tasks):
            if task.get("id") == task_id:
                tasks[i] = updated_task

                with open(self.file_path, "w") as f:
                    json.dump(tasks, f, indent=2)

                return updated_task
        raise ValueError("Task not found")

    def delete_task(self, task_id):
        tasks = self.get_tasks()
        for i, task in enumerate(tasks):
            if task.get("id") == task_id:
                tasks.pop(i)
                with open(self.file_path, "w") as f:
                    json.dump(tasks, f, indent=2)
                return
        raise ValueError("Task not found")

