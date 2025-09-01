import json
import requests


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
    
class Worker_AI():
    def __init__(self) -> None:
        self.key_api = '7u7cATCBx2R6jt2Qs_z958LzUGGSvquI23LpW-3h'
        key_bin = 'e8fb4d5fec908c5386b2dc336056ae78'
        root = 'https://api.cloudflare.com/client/v4/accounts/'
        self.model = '@cf/meta/llama-3-8b-instruct'
        self.url = f"{root}{key_bin}/ai/run/{self.model}"
        self.prompt = """
            You are an AI task solver. Your role is to provide extremely concise and precise solutions in Russian.
            **Hard Rule:**
            The sum of the character count of the original input task AND the character count of your solution MUST be less than 500.
            **Instructions:**
            1.  You will receive a task from the user.
            2.  You MUST calculate the character length of this input task.
            3.  Your solution must be so concise that its length + the input task's length < 500.
            4.  Your response MUST NOT repeat the task. Provide only the pure solution.

            Act strictly according to these instructions. If the input task is too long to allow for a solution within the limit, state this clearly.
            """
    
    def creating_solution_to_task(self, task):
        inputs = [{"role": "system", "content":  self.prompt},
                  { "role": "user", "content": task}]
        input = {"messages": inputs}
        solution = self.__post_json(input)
        return solution.json()['result']['response']

    def __post_json(self, data):
        new_data = json.dumps(data)

        headers = {"Authorization": f'Bearer {self.key_api}'}

        req = requests.post(self.url ,data=new_data, headers=headers)

        if req.status_code != 200:
            raise Exception(f"API Error {req}")
        
        return req
    
a = Worker_AI()
print(a.creating_solution_to_task('Как быстро охладить напиток без холодильника?'))
