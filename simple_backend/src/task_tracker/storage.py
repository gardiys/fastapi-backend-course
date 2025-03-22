import requests

class CloudStorage:
    def __init__(self, api_key, bin_id):
        self.api_key = api_key
        self.bin_id = bin_id
        self.base_url = "https://api.jsonbin.io/v3/b"

    def get_tasks(self):
        response = requests.get(
            f"{self.base_url}/{self.bin_id}",
            headers={"X-Master-Key": self.api_key}
        )
        return response.json()["record"]

    def save_tasks(self, tasks):
        response = requests.put(
            f"{self.base_url}/{self.bin_id}",
            headers={"X-Master-Key": self.api_key},
            json=tasks
        )
        return response.json()["record"]