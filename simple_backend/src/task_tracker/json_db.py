from fastapi import HTTPException
import json

class Json_db:
    def __init__(self, data_json):
        self.data_json = data_json

    def json_get_task(self):
        with open(self.data_json,"r+",encoding="utf-8") as file:
            load_data = json.load(file)
            return load_data

    def json_create_task(self, task_id, task_name, status_task):
        with open(self.data_json, "r+", encoding="utf-8") as file:
            loaded_data = json.load(file)
            if task_id in loaded_data:
                raise HTTPException(status_code=400, detail="Task with this ID already exists.")

            loaded_data[task_id] = [task_name, status_task]
            file.seek(0)
            file.truncate()
            json.dump(loaded_data, file, ensure_ascii=False, indent=4)

        return f'Task created'

    def json_update_task(self, task_id, task_name, status_task):

        with open(self.data_json, "r+", encoding="utf-8") as file:
            load_data = json.load(file)

            if task_id not in load_data:
                raise HTTPException(status_code=404, detail="Task not found.")

            load_data[task_id] = [task_name, status_task]
            file.seek(0)
            file.truncate()
            json.dump(load_data, file, ensure_ascii=False, indent=4)

        return f"Task {task_id} updated"


    def json_delete_task(self,task_id):
        with open(self.data_json, "r+", encoding="utf-8") as file:
            load_data = json.load(file)

            if task_id not in load_data:
                raise HTTPException(status_code=404, detail="Task not found.")

            del load_data[task_id]

            json.dump(load_data,file,ensure_ascii=False,indent=4)

