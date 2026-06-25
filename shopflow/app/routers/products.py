from typing import List, Optional

from fastapi import APIRouter, HTTPException, status

from app import database
from app.schemas import Product

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=List[Product])
def list_products(category: Optional[str] = None):
    items = database.list_products()
    if category:
        items = [p for p in items if p["category"] == category]
    return items


@router.get("/{product_id}", response_model=Product)
def get_product(product_id: int):
    product = database.get_product(product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return product
