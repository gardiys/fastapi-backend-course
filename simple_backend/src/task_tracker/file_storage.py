from pathlib import Path
import json


class FileStorage:
    def __init__(self, file_path: str = "C:\\Users\\sereg\\Desktop\\git_homework\\fastapi-backend-course\\simple_backend\\src\\task_tracker\\tasks.json"):
        self.file_path = Path(file_path)

    def _ensure_file_exists(self):
        """Создает файл, если его нет"""
        if not self.file_path.exists():
            self.file_path.write_text("[]", encoding="utf=8")

    def read_tasks(self):
        """Читает задачи из файла"""
        self._ensure_file_exists()
        try:
            with open(self.file_path, "r", encoding="utf=8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def save_tasks(self, tasks):
        """Сохраняет задачи в файл"""
        self._ensure_file_exists()
        with open(self.file_path, "w", encoding="utf=8") as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2)

    def get_next_id(self, tasks) -> int:
        """Получаем следующий ID для новой задачи"""
        return max(task["id"] for task in tasks) + 1 if tasks else 1

