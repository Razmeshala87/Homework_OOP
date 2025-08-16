import json
from io import StringIO
from pathlib import Path
from typing import Dict, Union

import pytest

from src.main import Category, LawnGrass, Product, Smartphone, load_data_from_json


@pytest.fixture
def sample_product() -> Product:
    """Фикстура для создания тестового продукта."""
    return Product("Тестовый товар", "Описание товара", 1000.0, 10)


@pytest.fixture
def sample_smartphone() -> Smartphone:
    """Фикстура для создания тестового смартфона."""
    return Smartphone(
        "Тестовый смартфон",
        "Описание",
        50000.0,
        3,
        "Высокая",
        "Модель X",
        "128GB",
        "Черный"
    )


@pytest.fixture
def sample_lawn_grass() -> LawnGrass:
    """Фикстура для создания тестовой газонной травы."""
    return LawnGrass(
        "Тестовая трава",
        "Описание",
        1000.0,
        20,
        "Россия",
        "14 дней",
        "Зеленый"
    )


@pytest.fixture
def sample_category() -> Category:
    """Фикстура для создания тестовой категории."""
    return Category("Тестовая категория", "Описание категории", [])


@pytest.fixture
def sample_json_file(tmp_path: Path) -> Path:
    """Фикстура для создания временного JSON файла."""
    data = [{
        "name": "Категория 1",
        "description": "Описание 1",
        "products": [{
            "name": "Товар 1",
            "description": "Описание товара 1",
            "price": 100.0,
            "quantity": 5
        }]
    }]
    file_path = tmp_path / "test_products.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f)
    return file_path


def test_price_setter_positive(sample_product: Product) -> None:
    """Тестирование установки положительной цены."""
    sample_product.price = 1500.0
    assert sample_product.price == 1500.0


def test_price_setter_negative_value(
        sample_product: Product,
        monkeypatch: pytest.MonkeyPatch
) -> None:
    """Тестирование попытки установки отрицательной цены."""
    monkeypatch.setattr('sys.stdin', StringIO('n\n'))
    original_price = sample_product.price
    sample_product.price = -500.0
    assert sample_product.price == original_price


def test_price_setter_lower_price_with_confirmation(
        sample_product: Product,
        monkeypatch: pytest.MonkeyPatch
) -> None:
    """Тестирование понижения цены с подтверждением."""
    monkeypatch.setattr('sys.stdin', StringIO('y\n'))
    sample_product.price = 800.0
    assert sample_product.price == 800.0


def test_price_setter_lower_price_without_confirmation(
        sample_product: Product,
        monkeypatch: pytest.MonkeyPatch
) -> None:
    """Тестирование понижения цены без подтверждения."""
    monkeypatch.setattr('sys.stdin', StringIO('n\n'))
    original_price = sample_product.price
    sample_product.price = 800.0
    assert sample_product.price == original_price


def test_new_product_with_existing_product(sample_product: Product) -> None:
    """Тестирование создания продукта, который уже существует."""
    existing_products = [sample_product]
    product_data: Dict[str, Union[str, float, int]] = {
        "name": "Тестовый товар",
        "description": "Новое описание",
        "price": 1200.0,
        "quantity": 5
    }
    new_product = Product.new_product(product_data, existing_products)
    assert new_product is sample_product


def test_new_product_without_existing_products() -> None:
    """Тестирование создания нового продукта без списка существующих."""
    product_data: Dict[str, Union[str, float, int]] = {
        "name": "Новый товар",
        "description": "Описание",
        "price": 500.0,
        "quantity": 3
    }
    new_product = Product.new_product(product_data)
    assert new_product.name == "Новый товар"


def test_load_data_from_json_file_not_found() -> None:
    """Тестирование загрузки данных из несуществующего файла."""
    categories = load_data_from_json("nonexistent_file.json")
    assert len(categories) == 0


def test_load_data_from_json_invalid_json(tmp_path: Path) -> None:
    """Тестирование загрузки данных из некорректного JSON."""
    file_path = tmp_path / "invalid.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("invalid json")
    categories = load_data_from_json(str(file_path))
    assert len(categories) == 0


def test_category_iterator(sample_category: Category, sample_product: Product) -> None:
    """Тестирование итератора по товарам категории."""
    sample_category.add_product(sample_product)
    iterator = iter(sample_category)

    # Проверяем первый и единственный элемент
    assert next(iterator) == sample_product

    # Проверяем остановку итерации
    with pytest.raises(StopIteration):
        next(iterator)


def test_category_iteration(sample_category: Category) -> None:
    """Тестирование итерации по категории с помощью цикла for."""
    products = [
        Product("Товар 1", "Описание 1", 100.0, 5),
        Product("Товар 2", "Описание 2", 200.0, 3)
    ]

    for product in products:
        sample_category.add_product(product)

    # Проверяем, что все товары доступны при итерации
    for i, product in enumerate(sample_category):
        assert product == products[i]


def test_category_list_conversion(sample_category: Category) -> None:
    """Тестирование преобразования категории в список товаров."""
    products = [
        Product("Товар 1", "Описание 1", 100.0, 5),
        Product("Товар 2", "Описание 2", 200.0, 3)
    ]

    for product in products:
        sample_category.add_product(product)

    # Проверяем преобразование в список
    assert list(sample_category) == products


def test_add_product_valid(sample_category: Category, sample_product: Product) -> None:
    """Тестирование добавления валидного продукта."""
    initial_count = Category.total_unique_products
    sample_category.add_product(sample_product)
    assert len(sample_category.products_list) == 1
    assert Category.total_unique_products == initial_count + 1


def test_add_product_invalid_type(sample_category: Category) -> None:
    """Тестирование попытки добавления невалидного типа."""
    with pytest.raises(TypeError):
        sample_category.add_product("это строка, а не продукт")  # type: ignore[arg-type]


def test_add_product_negative_quantity(sample_category: Category) -> None:
    """Тестирование попытки добавления продукта с отрицательным количеством."""
    with pytest.raises(ValueError):
        sample_category.add_product(Product("Товар", "Описание", 100.0, -5))


def test_add_product_existing(sample_category: Category, sample_product: Product) -> None:
    """Тестирование добавления существующего продукта."""
    initial_count = Category.total_unique_products
    sample_category.add_product(sample_product)
    sample_category.add_product(sample_product)
    assert len(sample_category.products_list) == 1
    assert Category.total_unique_products == initial_count + 1


def test_smartphone_creation(sample_smartphone: Smartphone) -> None:
    """Тестирование создания объекта Smartphone."""
    assert sample_smartphone.name == "Тестовый смартфон"
    assert sample_smartphone.model == "Модель X"
    assert sample_smartphone.memory == "128GB"


def test_lawn_grass_creation(sample_lawn_grass: LawnGrass) -> None:
    """Тестирование создания объекта LawnGrass."""
    assert sample_lawn_grass.name == "Тестовая трава"
    assert sample_lawn_grass.country == "Россия"
    assert sample_lawn_grass.germination_period == "14 дней"


def test_category_count(sample_category: Category) -> None:
    """Тестирование подсчета количества категорий."""
    initial_count = Category.total_categories
    _ = Category("Новая категория", "Описание", [])
    assert Category.total_categories == initial_count + 1


def test_load_data_from_json_success(sample_json_file: Path) -> None:
    """Тестирование успешной загрузки данных из JSON."""
    categories = load_data_from_json(str(sample_json_file))
    assert len(categories) == 1
    assert categories[0].name == "Категория 1"
    assert len(categories[0].products_list) == 1
    assert categories[0].products_list[0].name == "Товар 1"
