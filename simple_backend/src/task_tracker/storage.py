import json
import os


class TaskStorage:
    """Класс для работы с файлом задач"""

    def __init__(self, filename="tasks.json"):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                json.dump([], f)

    def load_tasks(self):
        """Загрузка задач из файла"""
        with open(self.filename, "r") as f:
            return json.load(f)

    def save_tasks(self, tasks):
        """Сохранение задач в файл"""
        with open(self.filename, "w") as f:
            json.dump(tasks, f, ensure_ascii=False, indent=4)
