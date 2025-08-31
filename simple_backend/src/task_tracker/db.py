from typing import List, Dict, Any, Optional, Union

from abc import ABCMeta, abstractmethod, abstractproperty

import os
import json

import requests


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

class CloudDB(absDB):
    def __init__(self) -> None:
        self.root = 'https://api.jsonbin.io/v3'
        self.key_api = '$2a$10$gkEEHNtdmq7FCAUiGF88k.IDmciahKhZmVL7ZBfbANA6US9nsQsu6'
        self.key_bin = '68b1c53ed0ea881f406a555a'
    
    def get_all(self) -> List[Dict[str, Any]]:
        return list(self.__get_json().values())

    def get(self, id) -> Dict[str, Any] | None:
        old_data = self.__get_json()
        if str(id) in old_data:
            return old_data[str(id)]
        return None

    def add(self, id, data) -> bool:
        old_data = self.__get_json()
        old_data[str(id)] = data
        self.__post_json(old_data)
        return True
    
    def delete(self, id) -> bool:
        data = self.__get_json()
        if str(id) in data:
            del data[str(id)]
            self.__post_json(data)
            return True
        return False

    def update(self, id, data) -> bool:
        all_data = self.__get_json()
        if str(id) in all_data:
            all_data[str(id)] = data
            self.__post_json(all_data)
            return True
        return False


    def __get_json(self):
        url = f"{self.root}/b/{self.key_bin}"
        headers = {
            'X-Master-Key': self.key_api,
            'X-Bin-Meta': 'false'
        }
        req = requests.get(url, headers=headers)
        if req.status_code != 200:
            raise Exception("API Error")
        return req.json()
        
    def __post_json(self, data):
        new_data = json.dumps(data)

        url = f"{self.root}/b/{self.key_bin}"
        headers = {
            'Content-Type': 'application/json',
            'X-Master-Key': self.key_api,
        }
        req = requests.put(url,data=new_data, headers=headers)
        if req.status_code != 200:
            raise Exception("API Error")
        return True

