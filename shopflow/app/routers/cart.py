from fastapi import APIRouter, HTTPException, status

from app import database
from app.schemas import PlaceOrderRequest
from app.services import pricing

router = APIRouter(prefix="/cart", tags=["cart"])


@router.post("/preview")
def preview(req: PlaceOrderRequest):
    """Return a price breakdown for a proposed cart without persisting it."""
    line_inputs = []
    for item in req.items:
        # Inline validation duplicated from utils.validation (see ISSUE-06).
        if item.quantity < 1 or item.quantity > 99:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid quantity",
            )
        product = database.get_product(item.product_id)
        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product {item.product_id} not found",
            )
        line_inputs.append({"product": product, "quantity": item.quantity})

    priced = pricing.price_order(line_inputs)
    return {
        "items": [i.model_dump() for i in priced["items"]],
        "subtotal": priced["subtotal"],
        "discount": priced["discount"],
        "tax": priced["tax"],
        "total": priced["total"],
    }
