"""Inventory availability and stock adjustments."""

from app import database


def is_in_stock(product: dict, quantity: int) -> bool:
    """Return whether ``quantity`` units of ``product`` can be fulfilled.

    BUG (ISSUE-02): this only checks that *some* stock exists and ignores the
    requested quantity, which allows customers to oversell beyond what is
    actually available.
    """
    return product["stock"] > 0


def reduce_stock(product_id: int, quantity: int) -> None:
    product = database.products[product_id]
    product["stock"] -= quantity
