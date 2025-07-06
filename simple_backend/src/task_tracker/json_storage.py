from os.path import getsize
from json import loads, dump


class JsonFileTaskStorage:
    def __init__(self, file):
        self.file = file

    def read_file(self):
        if getsize("data.json") > 0:
            with open(self.file, "r+") as json_file:
                return loads(json_file.read())
        return {}

    def change_file(self, task_data):
        with open(self.file, "r+") as json_file:
            json_file.seek(0)
            json_file.truncate(0)
            dump(task_data, json_file, indent=4)
