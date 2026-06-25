"""Pricing: line totals, bulk discounts, and tax."""

from typing import List

from app import config
from app.schemas import OrderItem


def price_line(unit_price: float, quantity: int):
    """Return ``(gross, discount)`` for a single line item.

    A bulk discount applies when the quantity reaches BULK_DISCOUNT_THRESHOLD.
    """
    gross = unit_price * quantity
    discount = 0.0
    # BUG (ISSUE-01): uses strict '>' so an order of exactly
    # BULK_DISCOUNT_THRESHOLD units does NOT receive the bulk discount.
    if quantity > config.BULK_DISCOUNT_THRESHOLD:
        discount = gross * config.BULK_DISCOUNT_RATE
    return round(gross, 2), round(discount, 2)


def calculate_tax(amount: float) -> float:
    """Sales tax on the given (post-discount) amount."""
    return round(amount * config.TAX_RATE, 2)


def price_order(line_inputs: List[dict]) -> dict:
    """Price a full order.

    ``line_inputs`` is a list of ``{"product": <dict>, "quantity": int}``.
    """
    items: List[OrderItem] = []
    subtotal = 0.0
    total_discount = 0.0

    for li in line_inputs:
        product = li["product"]
        quantity = li["quantity"]
        gross, discount = price_line(product["price"], quantity)
        line_total = round(gross - discount, 2)
        subtotal += gross
        total_discount += discount
        items.append(
            OrderItem(
                product_id=product["id"],
                name=product["name"],
                unit_price=product["price"],
                quantity=quantity,
                line_total=line_total,
            )
        )

    subtotal = round(subtotal, 2)
    total_discount = round(total_discount, 2)
    taxable = round(subtotal - total_discount, 2)
    tax = calculate_tax(taxable)
    total = round(taxable + tax, 2)

    return {
        "items": items,
        "subtotal": subtotal,
        "discount": total_discount,
        "tax": tax,
        "total": total,
    }
