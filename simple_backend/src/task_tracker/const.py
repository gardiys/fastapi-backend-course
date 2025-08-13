import enum

class TaskStatus(enum.Enum):
    PLANNED = 0 # Запланировано
    IN_PROGRESS = 1 # В работе
    COMPLETED = 2 # Выполнено