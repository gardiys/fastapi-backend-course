from stateless import Stateless


# При создании задачи указывается ее имя, id - автоинкремент, status - Открыта (так как только создана)
class MyTasks:
    def __init__(self, name):
        self.__state = Stateless()
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
        if not (tasks := self.__state.get_state()):
            return 1

        return tasks[-1].get("id") + 1
