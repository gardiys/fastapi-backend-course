
from utils.base_utils import BaseHTTPClient


class CloudflareService(BaseHTTPClient):
    MODEL: str = "@cf/meta/llama-3-8b-instruct"
    PROMPT_TEMPLATE: str = (
        "Generate a brief and clear solution for the following task:\n{description}\n"
        "Please summarize the key steps."
    )
    AUTHORIZATION_HEADER_NAME: str = "Authorization"

    def __init__(self, account_id: str, api_token: str):
        self.account_id = account_id
        self.api_token = api_token

    @property
    def base_url(self) -> str:
        return (
            f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/ai/run/"
        )

    @property
    def headers(self) -> str:
        return {self.AUTHORIZATION_HEADER_NAME: f"Bearer {self.api_token}"}

    async def get_solution(self, task_description: str) -> str:
        request_body = {
            "messages": [
                {
                    "role": "user",
                    "content": self.PROMPT_TEMPLATE.format(
                        description=task_description
                    ),
                }
            ]
        }
        response_body = await self._post(json=request_body, path=self.MODEL)
        return response_body["result"]["response"]
