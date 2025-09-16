from fastapi import FastAPI
from json_db_lite import JSONDatabase




class DataBase:
    def __init__(self):
        self.__db_client = JSONDatabase("db.json")

    @property
    def get_task(self):
        stat = self.__db_client.get_all_records()
        if stat:
            return stat
        return 'Database is empty'
    
    def create_task(self, text, status):
        stat = self.__db_client.get_all_records()
        if stat:
            task_id = len(stat) + 1
        else:
            task_id = 1
        self.__db_client.add_records({"id": task_id, "text": text, "status": status})
        return "Task created!"
    
    def update_task(self, task_id, text, status):
        stat = self.__db_client.get_all_records()
        if task_id <= len(stat):
            self.__db_client.update_record_by_key(
                upd_filter={"id": task_id}, new_data=[{"text": text, "status": status}]
            )
            return "Task changed!"
        return f"Task ID{task_id} is not in task list!"
    
    def delete_task(self, task_id):
        stat = self.__db_client.get_all_records()
        if task_id <= len(stat):
            self.__db_client.delete_record_by_key(key="id", value=task_id)
            return f"Task ID{task_id} deleted!"
        return f"Task ID{task_id} is not in task list!"


app = FastAPI()
db = DataBase()

@app.get("/tasks")
def get_tasks():
    result = db.get_task
    return result

@app.post("/tasks")
def create_task(text: str, status: bool) -> str:
    result = db.create_task(text, status)
    return result


@app.put("/tasks/{task_id}")
def update_task(task_id: int, text: str, status: bool) -> str:
    stat = db.update_task(task_id, text, status)
    return stat
    

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int) -> str:
    stat = db.delete_task(task_id)
    return stat