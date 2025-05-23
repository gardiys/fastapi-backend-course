from fastapi import HTTPException
import requests
from llm_client import LLM



class Json_db:
    def __init__(self, api_key, bin_id ):
        self.api_key = api_key
        self.bin_id = bin_id
        self.headers = {
            'Content-Type': 'application/json',
            'X-Master-Key': self.api_key
        }
        self.url = f'https://api.jsonbin.io/v3/b/{self.bin_id}'


    def json_get_task(self):
        response = requests.get(self.url, headers=self.headers)

        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to fetch data")
        return response.json()['record']


    def json_create_task(self, task_id, task_name, status_task):
        data = self.json_get_task()

        if task_id in data:
            raise HTTPException(status_code=400, detail="Task with this ID already exists.")

        llm_model = LLM(task_name)
        llm_response = llm_model.run()
        data[task_id] = {'task_name':task_name, 'status_task':status_task,'llm_solution': llm_response}

        self._save(data)

        return f'Task {task_id} created'

    def json_update_task(self, task_id, task_name, status_task):

        data = self.json_get_task()

        if task_id not in data:
            raise HTTPException(status_code=404, detail="Task not found.")

        llm_model = LLM(task_name)
        llm_response = llm_model.run()
        data[task_id] = {'task_name': task_name, 'status_task': status_task, 'llm_solution': llm_response}
        self._save(data)

        return f"Task {task_id} updated"


    def json_delete_task(self,task_id):
        data = self.json_get_task()

        if task_id not in data:
            raise HTTPException(status_code=404, detail="Task not found.")

        del data[task_id]
        self._save(data)

        return f'Task {task_id} was deleted'

    def _save(self, updated_data):

        response = requests.put(self.url, headers=self.headers, json=updated_data)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to save data")