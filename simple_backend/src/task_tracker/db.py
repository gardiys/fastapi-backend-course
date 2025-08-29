from typing import List, Dict, Any, Optional, Union

from abc import ABCMeta, abstractmethod, abstractproperty

import os
import json

class absDB():
    @abstractmethod
    def get_all(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get(self, id) -> Dict[str, Any] | None:
        pass

    @abstractmethod
    def add(self, id, data) -> bool:
        pass

    @abstractmethod
    def delete(self, id) -> bool:
        pass

    @abstractmethod
    def update(self, id, data) -> bool:
        pass

class ListDB(absDB):
    def init(self) -> None:
        self.tasks: Dict[int, Dict[str, Any]] = {}

    def get_all(self) -> List[Dict[str, Any]]:
        return list(self.tasks.values())

    def get(self, id) -> Dict[str, Any] | None:
        return self.tasks[id]

    def add(self, id, data) -> bool:
        self.tasks[id] = data
        return True

    def delete(self, id) -> bool:
        if id in self.tasks:
            del self.tasks[id]
            return True
        return False

    def update(self, id, data):
        if id in self.tasks:
            self.tasks[id].update(data)
            return True
        return False


class FileDB(absDB):
    def __init__(self) -> None:
        self.__name_file = 'my_db.json'
        print('File', self.__name_file)


    def get_all(self) -> List[Dict[str, Any]]:
        data = self.__read_json()
        return list(data.values())

    def get(self, id) -> Dict[str, Any] | None:
        data_from_file = self.__read_json()
        id = str(id)
        if id in data_from_file:
            return data_from_file[id]
        return None

    def add(self, id, data) -> bool:

        data_from_file = self.__read_json()
        data_from_file[id] = data
        self.__save_json(data_from_file)
        return True

    def delete(self, id) -> bool:
        data_from_file = self.__read_json()
        id = str(id)
        if id in data_from_file:
            del data_from_file[id]
            self.__save_json(data_from_file)
            return True
        return False

    def update(self, id, data):
        data_from_file = self.__read_json()
        id = str(id)
        if id in data_from_file:
            data_from_file[id] = data
            self.__save_json(data_from_file)
            return True
        return False

    def __save_json(self, data):
        with open(self.__name_file, 'w' '') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        return True

    def __read_json(self):
        print('File', self.__name_file)
        try:
            with open(self.__name_file, 'r' '') as file:
                print('File', file)
                try:
                    data = json.load(file)
                except json.JSONDecodeError :
                    print(12313)
                    self.__save_json({})
                    data = {}
        except FileNotFoundError:
            self.__save_json({})
            data = {}

        return data



list_db = FileDB()
# list_db.delete(2)
print(list_db.get_all())

# list_db.add(1, {1:1})
# list_db.add(2, {1:1})
# list_db.update(2, {4:1})
print(list_db.get_all())
print(list_db.get_all())

