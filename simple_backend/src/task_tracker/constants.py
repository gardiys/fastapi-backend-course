import os.path

TASKS_FILE_NAME: str = "tasks.json"
TASKS_FILE_PATH: str = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    TASKS_FILE_NAME,
)
