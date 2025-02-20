import requests
import json
import yaml


with open("settings.yml", "r", encoding="utf-8") as file:
    settings = yaml.safe_load(file)


class Stateless:
    def __init__(self):
        self.__gist_id = settings.get("gist_id")
        self.__github_token = settings.get("github_token")
        self.__gist_url = f"https://api.github.com/gists/{self.__gist_id}"

    @property
    def gist_url(self):
        return self.__gist_url

    @property
    def headers(self):
        return {
            "Authorization": f"token {self.__github_token}",
            "Accept": "application/vnd.github.v3+json",
        }

    def get_state(self):
        try:
            response = requests.get(url=self.gist_url, headers=self.headers)
            response.raise_for_status()
            response_json = response.json()
            result = json.loads(response_json["files"]["database.json"]["content"])
            return result
        except Exception as e:
            return {"error": str(e)}

    def update_state(self, tasks):
        try:
            data = {
                "files": {"database.json": {"content": json.dumps(tasks, indent=4)}}
            }
            response = requests.patch(
                url=self.gist_url, headers=self.headers, json=data
            )
            response.raise_for_status()
            return True
        except Exception as e:
            return {"error": str(e)}
