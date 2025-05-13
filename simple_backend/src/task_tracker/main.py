from fastapi import FastAPI

app = FastAPI()

@app.get("/tasks")
def get_tasks():
    pass

@app.post("/tasks")
def create_task(task):
    pass

@app.put("/tasks/{task_id}")
def update_task(task_id: int):
    pass

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    pass

#INFO:     Started server process [14848]
#INFO:     Waiting for application startup.
#INFO:     Application startup complete.
#INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
#INFO:     127.0.0.1:62006 - "GET /docs HTTP/1.1" 200 OK
#INFO:     127.0.0.1:62006 - "GET /openapi.json HTTP/1.1" 200 OK
#INFO:     127.0.0.1:62007 - "GET /tasks HTTP/1.1" 200 OK
