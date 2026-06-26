"""Order creation: ties together inventory checks and pricing."""

from datetime import datetime, timezone
from typing import List

from fastapi import HTTPException, status

from app import database
from app.schemas import CartItem, OrderStatus
from app.services import inventory, pricing


def create_order(customer_id: int, items: List[CartItem]) -> dict:
    line_inputs = []
    for item in items:
        product = database.get_product(item.product_id)
        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product {item.product_id} not found",
            )
        if not inventory.is_in_stock(product, item.quantity):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"'{product['name']}' is out of stock",
            )
        line_inputs.append({"product": product, "quantity": item.quantity})

    priced = pricing.price_order(line_inputs)

    for li in line_inputs:
        inventory.reduce_stock(li["product"]["id"], li["quantity"])

    order_id = database.next_order_id()
    order = {
        "id": order_id,
        "customer_id": customer_id,
        "items": [i.model_dump() for i in priced["items"]],
        "subtotal": priced["subtotal"],
        "discount": priced["discount"],
        "tax": priced["tax"],
        "total": priced["total"],
        "status": OrderStatus.pending.value,
        "created_at": datetime.now(timezone.utc),
        "payment_status": "unpaid",
        "payment_method": None,
    }
    database.orders[order_id] = order
    return order
