import json
from typing import Dict, List, Optional, Union


class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        """
        Сеттер для цены с проверками:
        1. Цена не должна быть <= 0
        2. При понижении цены требует подтверждения
        """
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        if new_price < self.__price:
            answer = input(
                f"Вы действительно хотите понизить цену с {self.__price} до {new_price}? (y/n): "
            )
            if answer.lower() != 'y':
                print("Изменение цены отменено")
                return

        self.__price = new_price

    def __repr__(self) -> str:
        return f"Product(name='{self.name}', price={self.__price}, quantity={self.quantity})"

    def __str__(self) -> str:
        return f"{self.name}, {self.__price} руб. Остаток: {self.quantity} шт."

    @classmethod
    def new_product(
            cls,
            product_data: Dict[str, Union[str, float, int]],
            products_list: Optional[List['Product']] = None
    ) -> 'Product':
        name = str(product_data['name'])
        description = str(product_data['description'])
        price = float(product_data['price'])
        quantity = int(product_data['quantity'])

        if products_list:
            for existing_product in products_list:
                if existing_product.name == name:
                    existing_product.quantity += quantity
                    existing_product.price = max(existing_product.price, price)
                    return existing_product

        return cls(name, description, price, quantity)


class Category:
    total_categories: int = 0
    total_unique_products: int = 0

    def __init__(self, name: str, description: str, products: List[Product]) -> None:
        self.name = name
        self.description = description
        self.__products = products  # Приватный атрибут

        Category.total_categories += 1
        Category.total_unique_products += len(products)

    def add_product(self, product: Product) -> None:
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты класса Product или его наследников")

        for existing_product in self.__products:
            if existing_product.name == product.name:
                existing_product.quantity += product.quantity
                existing_product.price = max(existing_product.price, product.price)
                return

        self.__products.append(product)
        Category.total_unique_products += 1

    @property
    def products(self) -> str:
        return "\n".join(str(p) for p in self.__products)

    @property
    def products_list(self) -> List[Product]:
        return self.__products

    def __repr__(self) -> str:
        return f"Category(name='{self.name}', products={len(self.__products)})"

    def __str__(self) -> str:
        total_quantity = sum(p.quantity for p in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."


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
    all_products: List[Product] = []

    for category_data in data:
        products = []
        for product_data in category_data['products']:
            product = Product.new_product({
                'name': str(product_data['name']),
                'description': str(product_data['description']),
                'price': float(product_data['price']),
                'quantity': int(product_data['quantity'])
            }, all_products)
            products.append(product)
            if product not in all_products:
                all_products.append(product)

        category = Category(
            name=str(category_data['name']),
            description=str(category_data['description']),
            products=products
        )
        categories.append(category)

    return categories


if __name__ == "__main__":
    # Демонстрация работы
    test_product = Product("Тестовый товар", "Описание", 1000, 10)
    print(f"Текущая цена: {test_product.price}")
    test_product.price = 1200
    print(f"Новая цена: {test_product.price}")

    # Демонстрация строкового представления
    print("\nДемонстрация строкового представления:")
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    category = Category("Смартфоны", "Описание категории", [product1, product2])

    print("\nСтроковое представление продукта:")
    print(product1)

    print("\nСтроковое представление категории:")
    print(category)

    print("\nСписок продуктов в категории:")
    print(category.products)

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
