from schemas import CloudFlare, Stateless


state = Stateless()
llm = CloudFlare()


# При создании задачи указывается ее имя, id - автоинкремент, status - Открыта (так как только создана)
class MyTasks:
    def __init__(self, name):
        self.__task_id = self.__initial_task_id()
        self.__task_name = name
        self.__status = "Открыта"
        self.solution = llm.send_prompt(name)

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
    def solution(self):
        return self.__solution

    @solution.setter
    def solution(self, text):
        if "error" in text:
            print(text)
            self.__solution = "-"
        else:
            self.__solution = text

    @property
    def info(self):
        return {
            "id": self.task_id,
            "name": self.task_name,
            "status": self.status,
            "solution": self.solution,
        }

    # функция для автоматической записи id задачи (id не повторяющийся)
    def __initial_task_id(self):
        if not (tasks := state.get_state()):
            return 1

        return tasks[-1].get("id") + 1
