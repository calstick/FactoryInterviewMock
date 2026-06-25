from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app import database
from app.auth import get_current_customer_id
from app.schemas import Order, PlaceOrderRequest
from app.services import orders as order_service

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", response_model=Order, status_code=status.HTTP_201_CREATED)
def place_order(
    req: PlaceOrderRequest,
    customer_id: int = Depends(get_current_customer_id),
):
    if not req.items:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Order must contain at least one item",
        )
    for item in req.items:
        # Inline validation duplicated from utils.validation (see ISSUE-06).
        if item.quantity < 1 or item.quantity > 99:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid quantity",
            )
    return order_service.create_order(customer_id, req.items)


@router.get("", response_model=List[Order])
def list_orders(customer_id: int = Depends(get_current_customer_id)):
    # FEATURE GAP (ISSUE-03): no filtering by status or date range yet.
    return [o for o in database.list_orders() if o["customer_id"] == customer_id]


@router.get("/{order_id}", response_model=Order)
def get_order(order_id: int):
    # SECURITY BUG (ISSUE-05): no authentication and no ownership check, so any
    # caller can read any customer's order by guessing the id (IDOR).
    order = database.orders.get(order_id)
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
    return order
