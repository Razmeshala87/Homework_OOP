import json
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Sequence, Union, cast


class ReprMixin:
    """Миксин для вывода информации о создании объекта."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        class_name = self.__class__.__name__
        params = ', '.join([f"{k}={v!r}" for k, v in self.__dict__.items()])
        print(f"Создан объект класса {class_name} с параметрами: {params}")


class BaseEntity(ABC):
    """Абстрактный базовый класс для сущностей с общей функциональностью."""

    @abstractmethod
    def __init__(self, name: str, description: str) -> None:
        self.name = name
        self.description = description

    @abstractmethod
    def __repr__(self) -> str:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass


class BaseProduct(ABC):
    __price: float  # Явное объявление атрибута для mypy

    @abstractmethod
    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    @property
    @abstractmethod
    def price(self) -> float:
        pass

    @price.setter
    @abstractmethod
    def price(self, new_price: float) -> None:
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def __add__(self, other: 'BaseProduct') -> float:
        pass

    @classmethod
    @abstractmethod
    def new_product(cls, product_data: Dict[str, Union[str, float, int]],
                    products_list: Optional[Sequence['BaseProduct']] = None) -> 'BaseProduct':
        pass


class Product(ReprMixin, BaseProduct):
    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        super().__init__(name=name, description=description, price=price, quantity=quantity)

    @property
    def price(self) -> float:
        return cast(float, getattr(self, '_BaseProduct__price'))

    @price.setter
    def price(self, new_price: float) -> None:
        current_price = cast(float, getattr(self, '_BaseProduct__price'))
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        if new_price < current_price:
            answer = input(
                f"Вы действительно хотите понизить цену с {current_price} до {new_price}? (y/n): ")
            if answer.lower() != 'y':
                print("Изменение цены отменено")
                return

        setattr(self, '_BaseProduct__price', new_price)

    def __repr__(self) -> str:
        return f"Product(name='{self.name}', price={self.price}, quantity={self.quantity})"

    def __str__(self) -> str:
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: BaseProduct) -> float:
        if not isinstance(other, BaseProduct):
            raise TypeError("Можно складывать только объекты класса Product или его наследников")

        if type(self) is not type(other):
            raise TypeError("Нельзя складывать товары разных классов")

        return self.price * self.quantity + other.price * other.quantity

    @classmethod
    def new_product(cls, product_data: Dict[str, Union[str, float, int]],
                    products_list: Optional[Sequence[BaseProduct]] = None) -> 'Product':
        name = str(product_data['name'])
        description = str(product_data['description'])
        price = float(product_data['price'])
        quantity = int(product_data['quantity'])

        if products_list:
            for existing_product in products_list:
                if existing_product.name == name:
                    existing_product.quantity += quantity
                    existing_product.price = max(existing_product.price, price)
                    return cast(Product, existing_product)

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


class Order(ReprMixin, BaseEntity):
    """Класс для представления заказа."""

    def __init__(self, product: Product, quantity: int) -> None:
        if not isinstance(product, Product):
            raise TypeError("Можно заказать только объекты классов Product или его наследников")
        if quantity <= 0:
            raise ValueError("Количество товара должно быть положительным числом")
        if quantity > product.quantity:
            raise ValueError("Недостаточно товара на складе")

        super().__init__(name=f"Заказ {product.name}", description=f"Заказ товара {product.name}")
        self.product = product
        self.quantity = quantity
        self.total_price = product.price * quantity
        product.quantity -= quantity  # Уменьшаем количество товара на складе

    def __repr__(self) -> str:
        return f"Order(product={self.product!r}, quantity={self.quantity}, total_price={self.total_price})"

    def __str__(self) -> str:
        return (f"Заказ: {self.product.name}, Количество: {self.quantity} шт., "
                f"Итого: {self.total_price} руб.")


class Category(ReprMixin, BaseEntity):
    """Класс для представления категории товаров."""
    total_categories: int = 0
    total_unique_products: int = 0

    def __init__(self, name: str, description: str, products: Sequence[Product]) -> None:
        super().__init__(name, description)
        self.__products: List[Product] = []

        for product in products:
            self.add_product(product)

        Category.total_categories += 1

    def add_product(self, product: Product) -> None:
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты классов Product или его наследников")

        if product.quantity <= 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")

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

    def __iter__(self) -> 'CategoryIterator':
        return CategoryIterator(self)

    def __repr__(self) -> str:
        return f"Category(name='{self.name}', products={len(self.__products)})"

    def __str__(self) -> str:
        total_quantity = sum(p.quantity for p in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."


class CategoryIterator:
    def __init__(self, category: Category) -> None:
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
        products: List[Product] = []
        for product_data in category_data['products']:
            product: Product
            if 'efficiency' in product_data:
                product = Smartphone(
                    name=str(product_data['name']),
                    description=str(product_data['description']),
                    price=float(product_data['price']),
                    quantity=int(product_data['quantity']),
                    efficiency=str(product_data['efficiency']),
                    model=str(product_data['model']),
                    memory=str(product_data['memory']),
                    color=str(product_data['color']))
            elif 'country' in product_data:
                product = LawnGrass(
                    name=str(product_data['name']),
                    description=str(product_data['description']),
                    price=float(product_data['price']),
                    quantity=int(product_data['quantity']),
                    country=str(product_data['country']),
                    germination_period=str(product_data['germination_period']),
                    color=str(product_data['color']))
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
    print("=== Тестирование классов ===")

    # Тестирование создания товара с нулевым количеством
    try:
        bad_product = Product("Неверный товар", "Описание", 100.0, 0)
    except ValueError as e:
        print(f"\nОжидаемая ошибка при создании товара: {e}")

    # Создаем тестовые продукты
    product1 = Product("Продукт1", "Описание продукта", 1200, 10)
    smartphone = Smartphone("Смартфон", "Описание", 50000, 3, "Высокая", "Модель X", "128GB", "Черный")
    grass = LawnGrass("Трава", "Описание", 1000, 20, "Россия", "14 дней", "Зеленый")

    # Создаем категорию
    category = Category("Тестовая категория", "Описание", [product1, smartphone])

    # Тестируем заказ
    try:
        order1 = Order(product1, 2)
        print("\nУспешный заказ:")
        print(order1)
        print(f"Остаток товара: {product1.quantity}")
    except (TypeError, ValueError) as e:
        print(f"Ошибка при создании заказа: {e}")

    try:
        order2 = Order(smartphone, 5)  # Пытаемся заказать больше, чем есть
    except ValueError as e:
        print(f"\nОжидаемая ошибка: {e}")

    # Выводим информацию о категории
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
