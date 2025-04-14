import json

TASKS_FILE = "tasks.json"


class TaskFile():
    @staticmethod
    def read_tasks_from_file():
        try:
            with open(TASKS_FILE, "r") as file:
                tasks = json.load(file)
        except FileNotFoundError:
            tasks = []
        return tasks

    @staticmethod
    def write_tasks_to_file(tasks):
        with open(TASKS_FILE, "w") as file:
            json.dump(tasks, file, indent=4)
