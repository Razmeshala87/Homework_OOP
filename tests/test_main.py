import json
import os
import sys
from io import StringIO
from pathlib import Path
from typing import List, Dict, Any

import pytest

from src.main import Category, Product, load_data_from_json


@pytest.fixture
def sample_product() -> Product:
    """Фикстура для создания тестового продукта"""
    return Product("Тестовый товар", "Описание товара", 1000.0, 10)


@pytest.fixture
def sample_category(sample_product: Product) -> Category:
    """Фикстура для создания тестовой категории"""
    return Category("Тестовая категория", "Описание категории", [sample_product])


@pytest.fixture
def sample_json_file(tmp_path: Path) -> Path:
    """Фикстура для создания временного JSON файла"""
    data = [
        {
            "name": "Категория 1",
            "description": "Описание 1",
            "products": [
                {
                    "name": "Товар 1",
                    "description": "Описание товара 1",
                    "price": 100.0,
                    "quantity": 5
                }
            ]
        }
    ]
    file_path = tmp_path / "test_products.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f)
    return file_path


def test_price_setter_positive(sample_product: Product) -> None:
    """Тестирование установки положительной цены"""
    sample_product.price = 1500.0
    assert sample_product.price == 1500.0


def test_price_setter_negative_value(sample_product: Product, monkeypatch: pytest.MonkeyPatch) -> None:
    """Тестирование попытки установки отрицательной цены"""
    monkeypatch.setattr('sys.stdin', StringIO('n\n'))  # Имитируем ввод 'n'
    original_price = sample_product.price
    sample_product.price = -500.0
    assert sample_product.price == original_price  # Цена не должна измениться


def test_price_setter_lower_price_with_confirmation(sample_product: Product, monkeypatch: pytest.MonkeyPatch) -> None:
    """Тестирование понижения цены с подтверждением"""
    monkeypatch.setattr('sys.stdin', StringIO('y\n'))  # Имитируем ввод 'y'
    sample_product.price = 800.0
    assert sample_product.price == 800.0


def test_price_setter_lower_price_without_confirmation(sample_product: Product, monkeypatch: pytest.MonkeyPatch) -> None:
    """Тестирование понижения цены без подтверждения"""
    monkeypatch.setattr('sys.stdin', StringIO('n\n'))  # Имитируем ввод 'n'
    original_price = sample_product.price
    sample_product.price = 800.0
    assert sample_product.price == original_price  # Цена не должна измениться


def test_new_product_with_existing_product(sample_product: Product) -> None:
    """Тестирование создания продукта, который уже существует"""
    existing_products = [sample_product]
    product_data = {
        "name": "Тестовый товар",
        "description": "Новое описание",
        "price": 1200.0,
        "quantity": 5
    }
    new_product = Product.new_product(product_data, existing_products)

    assert new_product is sample_product  # Должен вернуться существующий продукт
    assert new_product.quantity == 15  # 10 (было) + 5 (добавили)
    assert new_product.price == 1200.0  # Цена должна обновиться до большей


def test_new_product_without_existing_products() -> None:
    """Тестирование создания нового продукта без списка существующих"""
    product_data = {
        "name": "Новый товар",
        "description": "Описание",
        "price": 500.0,
        "quantity": 3
    }
    new_product = Product.new_product(product_data)

    assert new_product.name == "Новый товар"
    assert new_product.price == 500.0
    assert new_product.quantity == 3


def test_add_product_new(sample_category: Category) -> None:
    """Тестирование добавления нового продукта в категорию"""
    new_product = Product("Новый товар", "Описание", 500.0, 3)
    initial_count = len(sample_category._Category__products)  # Используем приватный атрибут
    sample_category.add_product(new_product)

    assert len(sample_category._Category__products) == initial_count + 1
    assert Category.total_unique_products == 2  # Должен увеличиться счетчик


def test_add_product_existing(sample_category: Category, sample_product: Product) -> None:
    """Тестирование добавления существующего продукта в категорию"""
    initial_count = len(sample_category._Category__products)
    initial_quantity = sample_product.quantity
    sample_category.add_product(sample_product)

    assert len(sample_category._Category__products) == initial_count  # Количество продуктов не изменилось
    assert sample_product.quantity == initial_quantity + sample_product.quantity  # Количество должно увеличиться


def test_load_data_from_json_success(sample_json_file: Path) -> None:
    """Тестирование успешной загрузки данных из JSON"""
    categories = load_data_from_json(str(sample_json_file))

    assert len(categories) == 1
    assert categories[0].name == "Категория 1"
    assert len(categories[0]._Category__products) == 1  # Используем приватный атрибут
    assert categories[0]._Category__products[0].name == "Товар 1"


def test_load_data_from_json_file_not_found() -> None:
    """Тестирование загрузки данных из несуществующего файла"""
    categories = load_data_from_json("nonexistent_file.json")
    assert len(categories) == 0


def test_load_data_from_json_invalid_json(tmp_path: Path) -> None:
    """Тестирование загрузки данных из некорректного JSON"""
    file_path = tmp_path / "invalid.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("invalid json")

    categories = load_data_from_json(str(file_path))
    assert len(categories) == 0
