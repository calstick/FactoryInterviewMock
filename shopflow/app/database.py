"""In-memory data store for the demo.

This is intentionally simple (plain dicts) so the demo runs with no external
database. Call ``reset()`` to reload seed data — used by both app startup and
the test suite.
"""

from copy import deepcopy
from typing import Dict, List

import seed_data

products: Dict[int, dict] = {}
customers: Dict[int, dict] = {}
credentials: Dict[str, dict] = {}  # email -> {password, customer_id}
orders: Dict[int, dict] = {}
_order_counter = {"value": 0}


def reset() -> None:
    """Reload all stores from seed data."""
    products.clear()
    customers.clear()
    credentials.clear()
    orders.clear()
    _order_counter["value"] = 0

    for p in deepcopy(seed_data.PRODUCTS):
        products[p["id"]] = p

    for c in deepcopy(seed_data.CUSTOMERS):
        password = c.pop("password")
        customers[c["id"]] = c
        credentials[c["email"]] = {"password": password, "customer_id": c["id"]}


def next_order_id() -> int:
    _order_counter["value"] += 1
    return _order_counter["value"]


def list_products() -> List[dict]:
    return list(products.values())


def get_product(product_id: int):
    return products.get(product_id)


def list_orders() -> List[dict]:
    return list(orders.values())


# Load seed data on import.
reset()
