from fastapi import FastAPI
from json_storage import JsonFileTaskStorage
from basehttpclient import GistAPI, CloudFlare


app = FastAPI()
gist = GistAPI()
ai_advice = CloudFlare()


# До github gists использовался класс для работы с json-файлом,
# хранящемся локально
# json_file = JsonFileTaskStorage("data.json")
# task_data = json_file.read_file()


@app.get("/tasks")
def get_tasks():
    task_data = gist.parse()

    if task_data:
        res = ""
        for task in task_data.values():
            res += (f"Task {task[0]}."
                    f" Status: {task[1]}."
                    f" Ai advice: {task[2]}")
        return res
    return "No tasks yet."


@app.post("/tasks")
def create_task(task_id: str, task_name: str, status: str):
    task_data = gist.parse()
    if str(task_id) not in task_data:
        advice = ai_advice.run(task_name)
        task_data[task_id] = [task_name, status, advice]
        gist.patch(task_data)

        return (f"Task {task_data[task_id][0]} created. "
                f"Ai advice is {advice}.")
    return f"Task with id {task_id} already exists."


@app.put("/tasks/{task_id}")
def update_task(task_id: str, new_status: str):
    task_data = gist.parse()
    if str(task_id) in task_data:
        task_data[task_id] = [task_data[task_id][0],
                              new_status,
                              task_data[task_id][2]]
        gist.patch(task_data)
        return f"Task {task_data[task_id][0]} status has been changed to {new_status}"
    return "No such task."


@app.delete("/tasks/{task_id}")
def delete_task(task_id: str):
    task_data = gist.parse()
    if str(task_id) in task_data:
        task_name = task_data.pop(str(task_id))[0]
        gist.patch(task_data)

        return f"Task {task_name} has been deleted."
    return f"Task id {task_id} not found"
