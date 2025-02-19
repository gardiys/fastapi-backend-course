from db import DataBase

# При создании задачи указывается ее имя, id - автоинкремент, status - Открыта (так как только создана)
class MyTasks:
    def __init__(self, name):
        self.__db = DataBase("database.json")
        self.__task_id = self.__initial_task_id()
        self.__task_name = name
        self.__status = "Открыта"

    @property
    def task_id(self):
        return self.__task_id

    @property
    def task_name(self):
        return self.__task_name

    @task_name.setter
    def task_name(self, name):
        if name:
            self.__task_name = name

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status):
        self.__status = status

    @property
    def info(self):
        return {"id": self.task_id, "name": self.task_name, "status": self.status}

    # функция для автоматической записи id задачи (id не повторяющийся)
    def __initial_task_id(self):
        if not (tasks := self.__db.get_data()):
            return 1

        return tasks[-1].get("id") + 1
