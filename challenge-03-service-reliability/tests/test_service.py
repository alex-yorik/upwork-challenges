"""Baseline tests. Add regression tests as part of the challenge."""

import sqlite3
from src.db import OrderRepository
from src.service import process_order


def make_repository():
    connection = sqlite3.connect(":memory:")
    repository = OrderRepository(connection)
    repository.create_schema()
    return repository


def make_order():
    return {
        "order_id": "ORD-1",
        "customer": "Alice",
        "total": 15.5,
        "items": [{"sku": "SKU-1", "quantity": 2}],
    }


def test_valid_order_is_saved():
    repository = make_repository()
    assert process_order(make_order(), repository) is True
    assert repository.count_orders() == 1
    assert repository.count_items() == 1


def test_missing_customer_is_rejected():
    repository = make_repository()
    order = make_order()
    order["customer"] = ""
    assert process_order(order, repository) is False
    assert repository.count_orders() == 0
