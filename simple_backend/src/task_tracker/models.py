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

    def __initial_task_id(self):
        if not MyTasks.all_tasks:
            return 1

        return MyTasks.all_tasks[-1].__task_id + 1
