import json
import os

def load_books(filename='library.json'):
    """
    Загрузка списка книг из JSON-файла.
    Возвращает список книг (каждая книга - это словарь).
    """
    if not os.path.isfile(filename):
        return []
    with open(filename, 'r', encoding='utf-8') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []

def save_books(books, filename='library.json'):
    """
    Сохранение списка книг в JSON-файл.
    """
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(books, file, ensure_ascii=False, indent=4)

def list_books(books):
    """
    Возвращает строку со списком всех книг.
    """
    if not books:
        return "Библиотека пуста."
    result_lines = []
    for idx, book in enumerate(books, start=1):
        result_lines.append(f"{idx}. {book['title']} | {book['author']} | {book['year']}")
    return "\n".join(result_lines)

def add_book(books, title, author, year):
    """
    Принимает текущий список книг и данные о новой книге.
    Возвращает новый список, в котором добавлена новая книга.
    """
    new_book = {
        'title': title,
        'author': author,
        'year': year
    }
    # Создаём НОВЫЙ список, добавляя new_book
    return books + [new_book]

def remove_book(books, title):
    """
    Принимает текущий список книг и название книги для удаления.
    Возвращает новый список без книги, у которой совпадает название.
    """
    # Фильтруем список: оставляем только те книги, у которых название не совпадает с переданным
    return [book for book in books if book['title'].lower() != title.lower()]

def search_books(books, keyword):
    """
    Поиск книг по ключевому слову (ищется в названии и авторе).
    Возвращает отфильтрованный список.
    """
    keyword_lower = keyword.lower()
    return [
        book for book in books
        if keyword_lower in book['title'].lower() or keyword_lower in book['author'].lower()
    ]

def main():
    """
    Точка входа в программу: здесь мы загружаем книги, 
    показываем меню и обрабатываем ввод пользователя.
    """
    books = load_books()  # Загрузили список книг из JSON

    while True:
        print("\n=== Управление онлайн-библиотекой ===")
        print("1. Показать все книги")
        print("2. Добавить книгу")
        print("3. Удалить книгу")
        print("4. Поиск книг")
        print("5. Выйти")

        choice = input("Выберите действие (1-5): ").strip()

        if choice == '1':
            print("\nСписок книг:")
            print(list_books(books))

        elif choice == '2':
            print("\nДобавление новой книги:")
            title = input("Введите название: ").strip()
            author = input("Введите автора: ").strip()
            year = input("Введите год издания: ").strip()

            # Получаем новый список с добавленной книгой
            new_books = add_book(books, title, author, year)
            books = new_books  # Обновляем переменную, чтобы сохранить изменения
<<<<<<< HEAD
            saving_books(books)  # Сразу сохраняем в файл
=======
            save_books(books)  # Сразу сохраняем в файл
>>>>>>> upstream/main
            print("Книга добавлена!")

        elif choice == '3':
            print("\nУдаление книги:")
            title_to_remove = input("Введите название книги, которую хотите удалить: ").strip()

            new_books = remove_book(books, title_to_remove)
<<<<<<< HEAD
            if len(new_books) > len(books):
                books = new_books
                saving_books(books)
=======
            if len(new_books) < len(books):
                books = new_books
                save_books(books)
>>>>>>> upstream/main
                print("Книга удалена!")
            else:
                print("Книга с таким названием не найдена.")

        elif choice == '4':
            print("\nПоиск книг:")
            keyword = input("Введите ключевое слово для поиска (в названии или авторе): ").strip()
            found_books = search_books(books, keyword)
            if found_books:
                print("\nНайденные книги:")
                print(list_books(found_books))
            else:
                print("Ничего не найдено.")

<<<<<<< HEAD
        elif choice == '6':
=======
        elif choice == '5':
>>>>>>> upstream/main
            print("Выход из программы.")
            break

        else:
            print("Некорректный ввод. Попробуйте ещё раз.")

<<<<<<< HEAD





if __name__ == "__main__":
    main()
=======
if __name__ == "__main__":
    main()
>>>>>>> upstream/main
