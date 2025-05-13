# Напишите класс для работы с файлом хранения задач в task_tracker
# и измените код проекта так, чтобы он работал с объектом этого класса.
import json


class TaskStorage:
    def __init__(self, file_path='tasks.json'):
        self.file_path = file_path

    def get_all_tasks(self):
        try:
            with open(self.file_path, 'r', encoding = 'utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_all_tasks(self, tasks):
        with open(self.file_path, 'w', encoding = 'utf-8') as f:
            json.dump(tasks, f, indent = 4, ensure_ascii = False)

    def create_new_task(self, title: str):
        tasks = self.get_all_tasks()
        new_id = max((task['id'] for task in tasks), default=-1) + 1
        new_task = {"id": new_id, "title": title, "status": 0}
        tasks.append(new_task)
        self.save_all_tasks(tasks)
        return new_task

    def update_task(self, task_id: int, title: str, status: int):
        tasks = self.get_all_tasks()
        for task in tasks:
            if task['id'] == task_id:
                task['title'] = title
                task['status'] = status
                self.save_all_tasks(tasks)
                return task
        return None

    def remove_task(self, task_id: int):
        tasks = self.get_all_tasks()
        for task in tasks:
            if task["id"] == task_id:
                deleted = task
                tasks.remove(task)
                self.save_all_tasks(tasks)
                return deleted
        return None

