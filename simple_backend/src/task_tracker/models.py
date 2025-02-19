import json

class MyTasks:
    all_tasks = []

    def __init__(self, name):
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
        return {
            "id": self.task_id,
            "name": self.task_name,
            "status": self.status
        }

    def __initial_task_id(self):
        try:
            with open("database.json", "r", encoding="utf-8") as file:
                data = json.load(file)
        except:
            return 1

        return data[-1].get("id") + 1
