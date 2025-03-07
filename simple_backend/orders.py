
class Order:
    TAX_RATE = 0.08  # 8% налог
    SERVICE_CHARGE = 0.05  # 5% сервисный сбор

    def __init__(self, customer):
        self.customer = customer
        self.dishes = []
    
    def add_dish(self, dish):
        if isinstance(dish, Dish):
            self.dishes.append(dish)
        else:
            raise ValueError("Можно добавлять только объекты класса Dish.")
    
    def remove_dish(self, dish):
        if dish in self.dishes:
            self.dishes.remove(dish)
        else:
            raise ValueError("Такого блюда нет в заказе.")

    def calculate_total(self):
        return sum(dish.price for dish in self.dishes)


    def final_total(self):
        total_after_discount = self.apply_discount()
        total_with_tax = total_after_discount * (1 + Order.TAX_RATE)
        final_total = total_with_tax * (1 + Order.SERVICE_CHARGE)
        return final_total

    def apply_discount(self):
        discount_rate = self.customer.get_discount() / 100
        return self.calculate_total() * (1 - discount_rate)

    def __str__(self):
        dish_list = "\n".join([str(dish) for dish in self.dishes])
        return f"Order for {self.customer.name}:\n{dish_list}\nTotal: ${self.final_total():.2f}"


class GroupOrder(Order):
    def __init__(self, customers):
        super().__init__(customer=None)  # Групповой заказ не привязан к одному клиенту
        self.customers = customers

    def split_bill(self):
        if not self.customers:
            raise ValueError("Нет клиентов для разделения счета.")
        total = self.final_total()
        return total / len(self.customers)

    def __str__(self):
        customer_list = ", ".join([customer.name for customer in self.customers])
        dish_list = "\n".join([str(dish) for dish in self.dishes])
        return f"Group Order for {customer_list}:\n{dish_list}\nTotal: ${self.final_total():.2f}"
  
class Dish:
    def __init__(self, name, price, category):
        self.name = name
        self.price = price
        self.category = category

    def __str__(self):
        return f"Dish: {self.name}, Category: {self.category}, Price: ${self.price:.2f}"

class Customer:
    def __init__(self, name, membership="Regular"):
        self.name = name
        self.membership = membership

    def get_discount(self):
        if self.membership == "VIP":
            return 10  # VIP клиенты получают 10% скидки
        return 0  # Обычные клиенты не получают скидки

    def __str__(self):
        return f"Customer: {self.name}, Membership: {self.membership}"
# Пример использования

# Создаем блюда
pizza = Dish("Pizza", 12, "Main Course")
ice_cream = Dish("Ice Cream", 5, "Dessert")
coffee = Dish("Coffee", 3, "Drink")

# Создаем клиентов
regular_customer = Customer("Alice", "Regular")
vip_customer = Customer("Bob", "VIP")

# Индивидуальный заказ
order1 = Order(regular_customer)
order1.add_dish(pizza)
order1.add_dish(ice_cream)

print(order1)  # Вывод информации о заказе
print(f"Final Total: ${order1.final_total():.2f}")  # Итоговая стоимость

# Групповой заказ
group_order = GroupOrder([regular_customer, vip_customer])
group_order.add_dish(pizza)
group_order.add_dish(ice_cream)
group_order.add_dish(coffee)

print(group_order)  # Вывод информации о групповом заказе
print(f"Split Bill: ${group_order.split_bill():.2f} per person")  # Стоимость на каждого