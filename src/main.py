import json
import os
from typing import List


class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

    def __repr__(self) -> str:
        return f"Product(name='{self.name}', price={self.price}, quantity={self.quantity})"


class Category:
    total_categories: int = 0
    total_unique_products: int = 0

    def __init__(self, name: str, description: str, products: List['Product']) -> None:
        self.name = name
        self.description = description
        self.products = products

        Category.total_categories += 1
        Category.total_unique_products += len(products)

    def __repr__(self) -> str:
        return f"Category(name='{self.name}', products={len(self.products)})"


def load_data_from_json(filename: str) -> List[Category]:
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Ошибка: файл {filename} не найден!")
        return []
    except json.JSONDecodeError:
        print(f"Ошибка: файл {filename} содержит некорректный JSON!")
        return []

    categories: List[Category] = []
    for category_data in data:
        products = [
            Product(
                name=product_data['name'],
                description=product_data['description'],
                price=product_data['price'],
                quantity=product_data['quantity']
            )
            for product_data in category_data['products']
        ]
        category = Category(
            name=category_data['name'],
            description=category_data['description'],
            products=products
        )
        categories.append(category)

    return categories


if __name__ == "__main__":
    # Получаем путь к директории src
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Поднимаемся на уровень выше (в Homework_OOP) и идем в папку data
    json_path = os.path.join(current_dir, '..', 'data', 'products.json')
    # Нормализуем путь (убираем ../)
    json_path = os.path.normpath(json_path)

    print(f"Пытаемся загрузить файл по пути: {json_path}")  # Для отладки

    categories = load_data_from_json(json_path)

    if categories:
        print("\nЗагруженные категории:")
        for category in categories:
            print(f"\n- {category.name} ({len(category.products)} товаров)")
            for product in category.products:
                print(f"  • {product.name} - {product.price} руб. (осталось: {product.quantity})")

        print("\nОбщая статистика:")
        print(f"Всего категорий: {Category.total_categories}")
        print(f"Всего уникальных товаров: {Category.total_unique_products}")
    else:
        print("\nНе удалось загрузить данные. Проверьте:")
        print(f"1. Существует ли файл: {json_path}")
        print("2. Корректно ли его содержимое (валидный JSON)")

# if __name__ == "__main__":
#     product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
#     product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
#     product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)
#
#     print(product1.name)
#     print(product1.description)
#     print(product1.price)
#     print(product1.quantity)
#
#     print(product2.name)
#     print(product2.description)
#     print(product2.price)
#     print(product2.quantity)
#
#     print(product3.name)
#     print(product3.description)
#     print(product3.price)
#     print(product3.quantity)
#
#     category1 = Category(
#         "Смартфоны",
#         "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
#         [product1, product2, product3],
#     )
#
#     print(category1.name == "Смартфоны")
#     print(category1.description)
#     print(len(category1.products))
#     print(category1.category_count)
#     print(category1.product_count)
#
#     product4 = Product('55" QLED 4K', "Фоновая подсветка", 123000.0, 7)
#     category2 = Category(
#         "Телевизоры",
#         "Современный телевизор, который позволяет наслаждаться просмотром, станет вашим другом и помощником",
#         [product4],
#     )
#
#     print(category2.name)
#     print(category2.description)
#     print(len(category2.products))
#     print(category2.products)
#
#     print(Category.category_count)
#     print(Category.product_count)
