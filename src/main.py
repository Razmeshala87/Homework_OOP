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
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        if new_price < self.__price:
            answer = input(f"Вы действительно хотите понизить цену с {self.__price} до {new_price}? (y/n): ")
            if answer.lower() != 'y':
                print("Изменение цены отменено")
                return

        self.__price = new_price

    def __repr__(self) -> str:
        return f"Product(name='{self.name}', price={self.price}, quantity={self.quantity})"

    def __str__(self) -> str:
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: 'Product') -> float:
        if not isinstance(other, Product):
            raise TypeError("Можно складывать только объекты класса Product или его наследников")

        if type(self) != type(other):
            raise TypeError("Нельзя складывать товары разных классов")

        return self.price * self.quantity + other.price * other.quantity

    @classmethod
    def new_product(cls, product_data: Dict[str, Union[str, float, int]],
                    products_list: Optional[List['Product']] = None) -> 'Product':
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


class Smartphone(Product):
    def __init__(
            self,
            name: str,
            description: str,
            price: float,
            quantity: int,
            efficiency: str,
            model: str,
            memory: str,
            color: str
    ) -> None:
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

    def __repr__(self) -> str:
        return (f"Smartphone(name='{self.name}', price={self.price}, quantity={self.quantity}, "
                f"efficiency='{self.efficiency}', model='{self.model}', "
                f"memory='{self.memory}', color='{self.color}')")

    def __str__(self) -> str:
        return (f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт. "
                f"(Модель: {self.model}, Память: {self.memory})")


class LawnGrass(Product):
    def __init__(
            self,
            name: str,
            description: str,
            price: float,
            quantity: int,
            country: str,
            germination_period: str,
            color: str
    ) -> None:
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def __repr__(self) -> str:
        return (f"LawnGrass(name='{self.name}', price={self.price}, quantity={self.quantity}, "
                f"country='{self.country}', germination_period='{self.germination_period}', "
                f"color='{self.color}')")

    def __str__(self) -> str:
        return (f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт. "
                f"(Страна: {self.country}, Срок прорастания: {self.germination_period})")


class CategoryIterator:
    def __init__(self, category: 'Category') -> None:
        self._category = category
        self._index = 0

    def __iter__(self) -> 'CategoryIterator':
        return self

    def __next__(self) -> Product:
        if self._index < len(self._category.products_list):
            product = self._category.products_list[self._index]
            self._index += 1
            return product
        raise StopIteration


class Category:
    total_categories: int = 0
    total_unique_products: int = 0

    def __init__(self, name: str, description: str, products: List[Product]) -> None:
        self.name = name
        self.description = description
        self.__products = []

        # Добавляем продукты через метод add_product для валидации
        for product in products:
            self.add_product(product)

        Category.total_categories += 1

    def add_product(self, product: Product) -> None:
        """Добавляет продукт в категорию с проверкой типа и количества."""
        if not isinstance(product, (Product, Smartphone, LawnGrass)):
            raise TypeError("Можно добавлять только объекты классов Product, Smartphone или LawnGrass")

        if not issubclass(type(product), Product):
            raise TypeError("Объект должен быть подклассом Product")

        if product.quantity <= 0:
            raise ValueError("Количество товара должно быть положительным числом")

        # Объединяем с существующим продуктом, если есть
        for existing_product in self.__products:
            if existing_product.name == product.name:
                existing_product.quantity += product.quantity
                existing_product.price = max(existing_product.price, product.price)
                return

        # Добавляем новый продукт
        self.__products.append(product)
        Category.total_unique_products += 1

    @property
    def products(self) -> str:
        return "\n".join(str(p) for p in self.__products)

    @property
    def products_list(self) -> List[Product]:
        return self.__products

    def __iter__(self) -> CategoryIterator:
        return CategoryIterator(self)

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
            if 'efficiency' in product_data:
                product = Smartphone(
                    name=str(product_data['name']),
                    description=str(product_data['description']),
                    price=float(product_data['price']),
                    quantity=int(product_data['quantity']),
                    efficiency=str(product_data['efficiency']),
                    model=str(product_data['model']),
                    memory=str(product_data['memory']),
                    color=str(product_data['color'])
                )
            elif 'country' in product_data:
                product = LawnGrass(
                    name=str(product_data['name']),
                    description=str(product_data['description']),
                    price=float(product_data['price']),
                    quantity=int(product_data['quantity']),
                    country=str(product_data['country']),
                    germination_period=str(product_data['germination_period']),
                    color=str(product_data['color'])
                )
            else:
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
    print("=== Тестирование защиты добавления продуктов в категорию ===")

    # Создаем тестовые продукты
    valid_product = Product("Валидный товар", "Описание", 100, 10)
    valid_smartphone = Smartphone("Смартфон", "Описание", 50000, 3, "Высокая", "Модель X", "128GB", "Черный")
    valid_grass = LawnGrass("Трава", "Описание", 1000, 20, "Россия", "14 дней", "Зеленый")

    # Создаем категорию
    category = Category("Тестовая категория", "Описание", [valid_product, valid_smartphone])

    # Успешное добавление
    try:
        category.add_product(valid_grass)
        print("Успешно добавлен:", valid_grass)
    except (TypeError, ValueError) as e:
        print("Ошибка:", e)

    # Попытка добавить неподходящий объект
    try:
        category.add_product("Это строка, а не продукт")
    except (TypeError, ValueError) as e:
        print("Ожидаемая ошибка при добавлении строки:", e)

    # Попытка добавить продукт с отрицательным количеством
    try:
        invalid_product = Product("Невалидный товар", "Описание", 100, -5)
        category.add_product(invalid_product)
    except (TypeError, ValueError) as e:
        print("Ожидаемая ошибка при отрицательном количестве:", e)

    # Вывод содержимого категории
    print("\nСодержимое категории:")
    for product in category:
        print(product)

    # Статистика
    print("\n=== Статистика ===")
    print(f"Всего категорий: {Category.total_categories}")
    print(f"Всего уникальных товаров: {Category.total_unique_products}")


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
