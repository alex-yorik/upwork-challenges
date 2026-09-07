"""SQLite persistence for the order service."""

import sqlite3


class OrderRepository:
    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection

    def create_schema(self) -> None:
        self.connection.execute(
            """CREATE TABLE IF NOT EXISTS orders (
                order_id TEXT NOT NULL,
                customer TEXT NOT NULL,
                total REAL NOT NULL
            )"""
        )
        self.connection.execute(
            """CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id TEXT NOT NULL,
                sku TEXT NOT NULL,
                quantity INTEGER NOT NULL
            )"""
        )
        self.connection.commit()

    def save_order(self, order: dict) -> None:
        self.connection.execute(
            "INSERT INTO orders (order_id, customer, total) VALUES (?, ?, ?)",
            (order["order_id"], order["customer"], order["total"]),
        )
        self.connection.commit()

    def save_items(self, order_id: str, items: list[dict]) -> None:
        for item in items:
            self.connection.execute(
                "INSERT INTO order_items (order_id, sku, quantity) VALUES (?, ?, ?)",
                (order_id, item["sku"], item["quantity"]),
            )
        self.connection.commit()

    def count_orders(self) -> int:
        return self.connection.execute("SELECT COUNT(*) FROM orders").fetchone()[0]

    def count_items(self) -> int:
        return self.connection.execute("SELECT COUNT(*) FROM order_items").fetchone()[0]
