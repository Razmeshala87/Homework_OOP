import json


class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

    def __repr__(self):
        return f"Product(name='{self.name}', price={self.price}, quantity={self.quantity})"


class Category:
    total_categories = 0
    total_unique_products = 0

    def __init__(self, name: str, description: str, products: list[Product]):
        self.name = name
        self.description = description
        self.products = products

        Category.total_categories += 1
        Category.total_unique_products += len(products)

    def __repr__(self):
        return f"Category(name='{self.name}', products={len(self.products)})"


# Загрузка данных из JSON файла
def load_data_from_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)

    categories = []
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


# Основной код
if __name__ == "__main__":
    categories = load_data_from_json('products.json')

    print("Загруженные категории:")
    for category in categories:
        print(f"- {category.name} ({len(category.products)} товаров)")
        for product in category.products:
            print(f"  • {product.name} - {product.price} руб. (осталось: {product.quantity})")

    print("\nОбщая статистика:")
    print(f"Всего категорий: {Category.total_categories}")
    print(f"Всего уникальных товаров: {Category.total_unique_products}")
