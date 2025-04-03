from fastapi import FastAPI
from functions import TaskTracker, TaskTrackerCloud
from cloudflare import CloudflareAI, inputs


app = FastAPI()
task_tracker = TaskTracker("dataj.json")  # Укажите имя файла для хранения задач
task_tracker_cloud = TaskTrackerCloud(
    api_key="$2a$10$U3LrdztF5Nfhb3MEMAl75ebPFA3/EPU56mXdNzbOBO.3mBgpRH4Ee",
    bin_id="67e7cb0f8a456b79667ede83"  # Omit or set to None to create a new bin
)

api_key = "0RoTLdhli-gaGPbyUC5V9CvmWs2bV9qntF0wuW-8"
cf_ai = CloudflareAI(api_key)
model = '@cf/meta/llama-3-8b-instruct'

@app.get("/tasks")
def get_tasks():
    return task_tracker_cloud.get_all_tasks()

@app.post("/tasks")
def create_task(task_id: int, name: str, status: str):
    new_task = {
        "id": task_id,
        "name": name,
        "status": status
    }
    inputs[1]['content'] = f'как выполнить эту задачу:{new_task["name"]}'
    output = cf_ai.run(model, inputs)
    response_text = output['result']['response']
    new_task["name"] = f'{new_task["name"]}. Инструкция к выполнению: {response_text}'
    return task_tracker_cloud.add_task(new_task)


@app.put("/tasks/{task_id}")
def update_task(task_id: int, name: str, status: str):
    return task_tracker_cloud.update_task(task_id, name, status)

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    return task_tracker_cloud.delete_task(task_id)
