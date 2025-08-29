from db import absDB, list_db


class TaskController:
    def __init__(self, data_base) -> None:
        self.__data_base = data_base

    def get_all_task(self):
        return self.__data_base.get_all()

    def get_task(self, id):
        return self.__data_base.get(id)

    def add_task(self, task):
        return self.__data_base.add(int(task['id']), task)

    def delete_task(self, id):
        return self.__data_base.delete(id)

    def update_task(self,id, task):
        return self.__data_base.update(id, task)

