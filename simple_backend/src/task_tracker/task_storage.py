import json
import os

class TaskStorage:
    def __init__(self, filename='tasks.json'):
        self.filename = filename
        self.tasks = self.load_tasks()

    def load_tasks(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                return json.load(file)
        return {"tasks": []}

    def save_tasks(self):
        with open(self.filename, 'w') as file:
            json.dump(self.tasks, file)

    def add_task(self, task):
        self.tasks["tasks"].append(task)
        self.save_tasks()

    def get_tasks(self):
        return self.tasks["tasks"]

    def update_task(self, task_id, updated_task):
        for index, task in enumerate(self.tasks["tasks"]):
            if task['id'] == task_id:
                self.tasks["tasks"][index] = updated_task
                self.save_tasks()
                return True
        return False

    def delete_task(self, task_id):
        self.tasks["tasks"] = [task for task in self.tasks["tasks"] if task['id'] != task_id]
        self.save_tasks()
