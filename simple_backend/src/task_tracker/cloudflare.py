import requests


class CloudflareAI:
    API_BASE_URL = "https://api.cloudflare.com/client/v4/accounts/208f1fab6615c60642471fa571b82b10/ai/run/"

    def __init__(self, api_key):
        self.headers = {"Authorization": f"Bearer {api_key}"}

    def run(self, model, inputs):
        input_data = {"messages": inputs}
        response = requests.post(f"{self.API_BASE_URL}{model}", headers=self.headers, json=input_data)

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.status_code, "message": response.text}


# Использование класса
api_key = "0RoTLdhli-gaGPbyUC5V9CvmWs2bV9qntF0wuW-8"  # Лучше хранить в переменных окружения
cf_ai = CloudflareAI(api_key)
model = '@cf/meta/llama-3-8b-instruct'

inputs = [
    {"role": "system", "content": "Ты ассистент который подсказывает как выполнить задачу в несколько шагов, кратко"},
    {"role": "user", "content": ""}
]

output = cf_ai.run(model, inputs)
print(output)

# curl -X GET "https://api.cloudflare.com/client/v4/user/tokens/verify" ^
#      -H "Authorization: Bearer 3-Gsldoa01q5PgphHA8BawN2LKWa-i6pg52LkEgM" ^
#      -H "Content-Type:application/json"

