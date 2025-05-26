from fastapi import HTTPException
from jsonbin_client import JsonDBClient
from llm_client import LLMClient

class Json_db:
    def __init__(self, api_key, bin_id):
        self.db = JsonDBClient(api_key, bin_id)
        self.llm = LLMClient("BTQqu4KbIo8l8drwgdNmDW1R1ZXvzL9bX3Um6LaK")

    def json_get_task(self):
        return self.db.get_data()

    def json_create_task(self, task_id, task_name, status_task):
        data = self.db.get_data()

        if task_id in data:
            raise HTTPException(status_code=400, detail="Task with this ID already exists.")

        llm_response = self.llm.explain(task_name)
        data[task_id] = {
            'task_name': task_name,
            'status_task': status_task,
            'llm_solution': llm_response
        }

        self.db.save_data(data)
        return f'Task {task_id} created'

    def json_update_task(self, task_id, task_name, status_task):
        data = self.db.get_data()

        if task_id not in data:
            raise HTTPException(status_code=404, detail="Task not found.")

        llm_response = self.llm.explain(task_name)
        data[task_id] = {
            'task_name': task_name,
            'status_task': status_task,
            'llm_solution': llm_response
        }

        self.db.save_data(data)
        return f'Task {task_id} updated'

    def json_delete_task(self, task_id):
        data = self.db.get_data()

        if task_id not in data:
            raise HTTPException(status_code=404, detail="Task not found.")

        del data[task_id]
        self.db.save_data(data)

        return f'Task {task_id} was deleted'
