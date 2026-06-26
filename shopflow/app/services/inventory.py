"""Inventory availability and stock adjustments."""

from app import database


def is_in_stock(product: dict, quantity: int) -> bool:
    """Return whether ``quantity`` units of ``product`` can be fulfilled."""
    return product["stock"] >= quantity


def reduce_stock(product_id: int, quantity: int) -> None:
    product = database.products[product_id]
    product["stock"] -= quantity
