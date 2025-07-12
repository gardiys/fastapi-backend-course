import aiohttp


class CloudflareService:
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
    def api_base_url(self) -> str:
        return (
            f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/ai/run/"
        )

    async def get_solution(self, task_description: str) -> str:
        async with aiohttp.ClientSession() as session:
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

            async with session.post(
                url=f"{self.api_base_url}{self.MODEL}",
                json=request_body,
                headers={self.AUTHORIZATION_HEADER_NAME: f"Bearer {self.api_token}"},
            ) as response:
                response_body = await response.json()
                return response_body["result"]["response"]
