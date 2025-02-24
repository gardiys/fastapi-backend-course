import json
from abc import ABC, abstractmethod

import requests
import yaml
from fastapi import HTTPException

with open("settings.yml", "r", encoding="utf-8") as file:
    settings = yaml.safe_load(file)


class BaseHTTPClient(ABC):
    account_id: str
    token: str
    base_url: str


    def __init__(self, account_id: str, token: str, base_url: str):
        self.account_id = account_id
        self.token = token
        self.base_url = base_url

    @abstractmethod
    def _headers(self):
        pass

    def _make_request(self, method, url, headers, **kwargs):
        try:
            response = requests.request(method, url, headers=headers, **kwargs)
            response.raise_for_status()

            return response.json()

        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

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

        super().__init__(account_id=account_id, token=token, base_url=url)

    def _headers(self):
        return {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json",
        }

    def get_state(self):
        try:
            response = self._make_request("GET", self.base_url, self._headers())
            return json.loads(response["files"]["database.json"]["content"])

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def update_state(self, tasks):
        try:
            data = {
                "files": {"database.json": {"content": json.dumps(tasks, indent=4)}}
            }

            response = self._make_request(
                "PATCH", self.base_url, self._headers(), json=data
            )

            return response

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


class CloudFlare(BaseHTTPClient):
    def __init__(self):
        account_id = settings.get("cloudflare_id")
        token = settings.get("cloudflare_token")
        url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/@cf/meta/llama-3-8b-instruct"

        super().__init__(account_id=account_id, token=token, base_url=url)

    def _headers(self):
        return {"Authorization": f"Bearer {self.token}"}

    def send_prompt(self, task_name):
        try:
            data = {
                "prompt": f"Объясни решение этой задачи на русском языке: {task_name}"
            }

            response = self._make_request(
                "POST", self.base_url, self._headers(), json=data
            )

            return response["result"]["response"]
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_state(self):
        raise NotImplementedError()

    def update_state(self, data):
        raise NotImplementedError()
