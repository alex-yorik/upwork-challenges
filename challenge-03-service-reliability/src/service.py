"""Order business logic."""

import sqlite3
from .db import OrderRepository


def validate_order(order: dict) -> bool:
    return bool(order.get("order_id") and order.get("customer") and order.get("items"))


def process_order(order: dict, repository: OrderRepository) -> bool:
    if not validate_order(order):
        return False

    try:
        repository.save_order(order)
        repository.save_items(order["order_id"], order["items"])
        return True
    except sqlite3.Error:
        return False
