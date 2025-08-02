import pytest
from src.main import Product, Category


@pytest.fixture
def sample_product():
    """Фикстура для создания тестового продукта."""
    return Product("Тестовый товар", "Описание", 1000.0, 10)


@pytest.fixture
def sample_category(sample_product):
    """Фикстура для создания тестовой категории с одним товаром."""
    return Category("Тестовая категория", "Описание", [sample_product])


def test_product_initialization(sample_product):
    """Проверяет корректность инициализации продукта."""
    assert sample_product.name == "Тестовый товар"
    assert sample_product.description == "Описание"
    assert sample_product.price == 1000.0
    assert sample_product.quantity == 10


def test_category_initialization(sample_category, sample_product):
    """Проверяет корректность инициализации категории."""
    assert sample_category.name == "Тестовая категория"
    assert sample_category.description == "Описание"
    assert len(sample_category.products) == 1
    assert sample_category.products[0] == sample_product


def test_total_products_count():
    """Проверяет подсчет общего количества уникальных товаров."""
    # Сбрасываем счетчики перед тестом
    Category.total_categories = 0
    Category.total_unique_products = 0

    # Создаем тестовые данные
    product1 = Product("Товар 1", "Описание 1", 100.0, 5)
    product2 = Product("Товар 2", "Описание 2", 200.0, 3)
    category1 = Category("Категория 1", "Описание", [product1, product2])
    category2 = Category("Категория 2", "Описание", [product1])

    # Проверяем счетчики
    assert Category.total_unique_products == 3  # 2 товара в первой категории + 1 во второй
    assert Category.total_categories == 2


def test_empty_category():
    """Проверяет создание категории без товаров."""
    Category.total_categories = 0  # Сброс счетчика
    empty_category = Category("Пустая категория", "Описание", [])

    assert len(empty_category.products) == 0
    assert Category.total_categories == 1
    assert Category.total_unique_products == 0  # Товаров нет


def test_product_repr(sample_product):
    """Проверяет строковое представление продукта."""
    assert repr(sample_product) == "Product(name='Тестовый товар', price=1000.0, quantity=10)"


def test_category_repr(sample_category):
    """Проверяет строковое представление категории."""
    assert repr(sample_category) == "Category(name='Тестовая категория', products=1)"
