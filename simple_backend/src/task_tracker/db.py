import json
import os


class DataBase:
    def __init__(self, filename):
        self.filename = filename

    @property
    def filename(self):
        return self.__filename

    @filename.setter
    def filename(self, filename):
        if os.path.exists(filename):
            self.__filename = filename
        else:
            raise Exception("Файла не существует!")

    def get_data(self):
        try:
            with open(self.__filename, "r", encoding="utf-8") as file:
                return json.load(file)

        except Exception as e:
            print(e)
            return None

    def save_changes(self, data):
        try:
            with open(self.__filename, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

            return True
        except Exception as e:
            print(e)
            return False
