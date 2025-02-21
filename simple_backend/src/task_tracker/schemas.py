import requests
import json
import yaml
from abc import ABC, abstractmethod


with open("settings.yml", "r", encoding="utf-8") as file:
    settings = yaml.safe_load(file)


class BaseHTTPClient(ABC):
    def __init__(self, account_id, token, url):
        self.__account_id = account_id
        self.__token = token
        self.__base_url = url

    @property
    def account_id(self):
        return self.__account_id

    @property
    def token(self):
        return self.__token

    @property
    def base_url(self):
        return self.__base_url

    @abstractmethod
    def _headers(self):
        pass

    def _make_request(self, method, url, headers, **kwargs):
        try:
            response = requests.request(method, url, headers=headers, **kwargs)
            response.raise_for_status()

            return response.json()

        except Exception as e:
            return {"error": str(e)}

    @abstractmethod
    def get_state(self):
        pass

    @abstractmethod
    def update_state(self, data):
        pass


class Stateless(BaseHTTPClient):
    def __init__(self):
        account_id = settings.get("gist_id")
        token = settings.get("github_token")
        url = f"https://api.github.com/gists/{account_id}"

        super().__init__(account_id, token, url)

    def _headers(self):
        return {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json",
        }

    def get_state(self):
        response = self._make_request("GET", self.base_url, self._headers())

        if "error" in response:
            return response

        return json.loads(response["files"]["database.json"]["content"])

    def update_state(self, tasks):
        data = {"files": {"database.json": {"content": json.dumps(tasks, indent=4)}}}

        response = self._make_request(
            "PATCH", self.base_url, self._headers(), json=data
        )

        return True if "error" not in response else response


class CloudFlare(BaseHTTPClient):
    def __init__(self):
        account_id = settings.get("cloudflare_id")
        token = settings.get("cloudflare_token")
        url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/@cf/meta/llama-3-8b-instruct"

        super().__init__(account_id, token, url)

    def _headers(self):
        return {"Authorization": f"Bearer {self.token}"}

    def send_prompt(self, task_name):
        data = {"prompt": f"Объясни решение этой задачи на русском языке: {task_name}"}

        response = self._make_request("POST", self.base_url, self._headers(), json=data)

        if "error" in response:
            return response

        return response["result"]["response"]

    def get_state(self):
        raise NotImplementedError()

    def update_state(self, data):
        raise NotImplementedError()
