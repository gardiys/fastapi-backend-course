import json

class Order:
    TAX_RATE = 0.08
    SERVICE_CHARGE = 0.05

    def __init__(self, customer):
        self.customer = customer
        self.dishes = []

    def add_dish(self, dish):
        self.dishes.append(dish)

    def remove_dish(self, dish):
        if dish in self.dishes:
            self.dishes.remove(dish)

    def calculate_total(self):
        return sum(dish.price for dish in self.dishes)

    def apply_discount(self):
        return self.calculate_total()

    def final_total(self):
        total_after_discount = self.apply_discount()
        total_with_tax = total_after_discount * (1 + Order.TAX_RATE)
        final_total = total_with_tax * (1 + Order.SERVICE_CHARGE)
        return final_total

    def __str__(self):
        dish_list = "\n".join([str(dish) for dish in self.dishes])
        return f"Order for {self.customer.name}:\n{dish_list}\nTotal: ${self.final_total():.2f}"


class GroupOrder(Order):
    def __init__(self, customers):
        super().__init__(customer=None)
        self.customers = customers

    def split_bill(self):
        if not self.customers:
            return 0
        total = self.final_total()
        return total / len(self.customers)


class Customer:
    def __init__(self, name, membership="Regular"):
        self.name = name
        self.membership = membership


def saving_books(books, filename="library.json"):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(books, file, ensure_ascii=False, indent=4)


def list_books(books):
    if not books:
        return "Библиотека пуста."
    result_lines = []
    for idx, book in enumerate(books, start=1):
        result_lines.append(f"{idx}. {book['title']} | {book['author']} | {book['year']}")
    return "\n".join(result_lines)


def add_book(books, title, author, year):
    books.append({"title": title, "author": author, "year": year})
    return books


def remove_book(books, title_to_remove):
    new_books = [b for b in books if b["title"] != title_to_remove]
    return new_books


def main():
    books = []
    while True:
        choice = input("Выберите действие (1-5): ")
        if choice == "1":
            title = input("Название книги: ")
            author = input("Автор: ")
            year = input("Год: ")
            books = add_book(books, title, author, year)
            saving_books(books)
            print("Книга добавлена!")
        elif choice == "2":
            title_to_remove = input("Название книги для удаления: ")
            new_books = remove_book(books, title_to_remove)
            if len(new_books) < len(books):
                books = new_books
                saving_books(books)
                print("Книга удалена!")
            else:
                print("Книга с таким названием не найдена.")
        elif choice == "3":
            print(list_books(books))
        elif choice == "4":
            print("Простое место для другой функции")
        elif choice == "5":
            print("Выход из программы.")
            break
        else:
            print("Некорректный ввод. Попробуйте ещё раз.")


if __name__ == "__main__":
    main()