import requests


class BaseHTTPClient:
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers

    def post_request(self, json_data):
        response = requests.post(url=self.url, json=json_data, headers=self.headers)
        response.raise_for_status()
        return response.json()


class TaskStorage(BaseHTTPClient):
    new_id = 0

    def read_tasks(self):
        response = requests.get(self.url)
        return response.json()

    def add_task(self, task_description, solution):
        task = {"task": task_description, "solution": solution, "status": False, "id": self.new_id}
        self.new_id += 1
        self.post_request(json_data=task)
        return self.new_id - 1

    def update_task(self, task_id, new_status=True):
        response = requests.patch(f'{self.url}/{task_id}', json={"status": new_status})
        return response.ok

    def delete_task(self, task_id):
        response = requests.delete(f'{self.url}/{task_id}')
        return response.ok


class Cloudflare(BaseHTTPClient):

    def ask_solution(self, task_description):
        json_message = {"messages": [
            {"role": "system", "content": "You are a friendly assistant that helps solve the task"},
            {"role": "user",
             "content": f"Please advise haw i can solve this task: {task_description}"}
        ]}
        return self.post_request(json_data=json_message)
