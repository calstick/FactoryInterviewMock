"""Shared request validation helpers."""

from fastapi import HTTPException, status

from app import config


def validate_quantity(quantity: int) -> None:
    if quantity < 1:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Quantity must be at least 1",
        )
    if quantity > config.MAX_LINE_QUANTITY:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Quantity may not exceed {config.MAX_LINE_QUANTITY}",
        )
