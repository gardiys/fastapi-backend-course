from model import Task
from typing import List
import json
import requests



class CloudflareWorkersAi:
    def __init__(self,task:Task,ai_agent:dict):
        self.task = task
        self.ai_agent = ai_agent


    def send_task_ai(self)->Task:
        API_BASE_URL = self.ai_agent["API_BASE_URL"]
        API_TOKEN = self.ai_agent["API_TOKEN"]
        model=self.ai_agent["model"]
        headers = {"Authorization": f"Bearer {API_TOKEN}"}
        input = {"messages": [
            {"role": "system", "content": f"Помоги решить задачу не задавая вопросов,ответ пиши краткий до 200 символов: {self.task.title}"},
        ]}
        response = requests.post(f"{API_BASE_URL}{model}", headers=headers, json=input)
        response_output = response.json()
        output_llm = response_output["result"]["response"]
        task_title_llm = self.task.title + " (Решение от AI агента: " + output_llm + ")"
        self.task.title = task_title_llm
        return self.task


