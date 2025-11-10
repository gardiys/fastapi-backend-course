from basehttp import BaseHTTPClient

class CloudFlareClient(BaseHTTPClient):
    inputs = [
        {"role": "system", "content":
            "Отвечай по-русски, кратко (1–2 предложения),"
            "как лучше выполнить задачу из списка дел. Без приветствий и воды."
            "Отвечай естественно, без вводных фраз вроде «Для выполнения задачи…», «Чтобы сделать…», «Следует…»."
            "Сразу переходи к сути,"
            "Если в задаче есть действие, пиши как"
            " будто даёшь понятную инструкцию или совет, а не академическое объяснение"}
    ]

    def __init__(self, api_token: str, account_id: str):
        super().__init__(
            base_url=f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run",
            headers={
                "Authorization": f"Bearer {api_token}",
                "Content-Type": "application/json"
            }
        )

    def generate_answer(self, task: str) -> str:
        data = {"messages": self.inputs + [{"role": "user", "content": task}]}
        result = self.post("@cf/meta/llama-3-8b-instruct", json=data)
        response_text = result["result"]["response"]

        if not response_text:
            raise ValueError("Пустой или некорректный ответ от CloudFlare AI")

        return response_text
