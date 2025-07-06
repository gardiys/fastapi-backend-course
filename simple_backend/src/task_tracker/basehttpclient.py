from dotenv import load_dotenv
import os
from abc import ABC, abstractmethod
import requests
from json import loads, dumps, JSONDecodeError

load_dotenv()
api_url = os.getenv("API_BASE_URL")
token_llm  = os.getenv("CLOUDFLARE_API_TOKEN")
gist_id = os.getenv("GIST_ID")
token_gist= os.getenv("GITHUB_TOKEN")
gist_url = f"https://api.github.com/gists/{gist_id}"


class BaseHttpClient(ABC):
    HEADERS_GIST = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token_gist}",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    HEADERS_LLM = {"Authorization": f"Bearer {token_llm}"}
    LLM_MODEL_NAME = "@cf/meta/llama-3-8b-instruct"

    @abstractmethod
    def parse(self, *args, **kwargs):
        pass


class CloudFlare(BaseHttpClient):


    @staticmethod
    def change_input(input_msg):
        inputs = [
            {"role": "system",
             "content": "You are a suggesting user how to get their tasks done, advise, help to find solution. "
                        "It must be short! 50 symbols limit! No nice talking, just solution!"},
            {"role": "user", "content": input_msg}]
        input_msg = {"messages": inputs}

        return input_msg

    def parse(self, input_msg):
        response_json = requests.post(f"{api_url}{self.LLM_MODEL_NAME}", headers=self.HEADERS_LLM,
                                      json=input_msg).json()
        return response_json

    def run(self, task_text: str):
        input_msg = self.change_input(task_text)
        response = self.parse(input_msg)
        result = response["result"]["response"]
        return result


class GistAPI(BaseHttpClient):

    def parse(self):
        parse_json = requests.get(gist_url, headers=self.HEADERS_GIST).json()
        try:
            task_data = loads(parse_json["files"]["data.json"]["content"])
        except JSONDecodeError:
            return {}
        else:
            return task_data

    def patch(self, new_data):
        data = {
            "description": "An updated gist description",
            "files": {
                "data.json": {
                    "content": dumps(new_data, indent=4)
                }
            }
        }
        print(requests.patch(gist_url, headers=self.HEADERS_GIST, json=data))


