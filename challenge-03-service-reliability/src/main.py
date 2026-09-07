"""Command-line entry point."""

import json
import sqlite3
from .db import OrderRepository
from .service import process_order


SAMPLE_ORDER = {
    "order_id": "ORD-1001",
    "customer": "Alice",
    "total": 29.90,
    "items": [
        {"sku": "BOOK-1", "quantity": 1},
        {"sku": "PEN-2", "quantity": 2},
    ],
}


def main() -> int:
    connection = sqlite3.connect(":memory:")
    repository = OrderRepository(connection)
    repository.create_schema()

    ok = process_order(SAMPLE_ORDER, repository)
    print(json.dumps({"success": ok, "orders": repository.count_orders(), "items": repository.count_items()}))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
