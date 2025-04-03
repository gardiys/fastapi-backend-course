import json


def file_load():
    try:
        with open('dataj.json', 'r', encoding='utf-8') as f:
            file = json.load(f)
            return file
    except FileNotFoundError:
        return 'файл не найден'

def file_save(data):
    try:
        with open('dataj.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            return 'данные сохранены'
    except IOError:
        return 'ошибка при записи файла'


