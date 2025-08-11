from model import Task


from base_http_client import BaseHTTPClient


class CloudflareWorkersAi(BaseHTTPClient):
    def __init__(self, task: Task, ai_agent: dict, timeout: int):
        self.task = task
        self.ai_agent = ai_agent
        super().__init__(self.ai_agent["API_BASE_URL"], timeout)

    def json_to_task(self, data: dict | list[dict]) -> Task | list[Task]:
        output_llm = data["result"]["response"]
        task_title_llm = self.task.title + " (Решение от AI агента: " + output_llm + ")"
        self.task.title = task_title_llm
        return self.task

    def send_task_ai(self) -> Task:
        API_TOKEN = self.ai_agent["API_TOKEN"]
        model = self.ai_agent["model"]
        headers = {"Authorization": f"Bearer {API_TOKEN}"}
        input = {
            "messages": [
                {
                    "role": "system",
                    "content": f"Помоги решить задачу не задавая вопросов,ответ пиши краткий до 200 символов: {self.task.title}",
                },
            ]
        }
        response_output = self.post(f"{model}", input, headers)
        return self.json_to_task(response_output)
