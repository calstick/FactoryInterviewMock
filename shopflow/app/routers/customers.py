from fastapi import APIRouter, Depends

from app import database
from app.auth import get_current_customer_id
from app.schemas import Customer

router = APIRouter(prefix="/customers", tags=["customers"])


@router.get("/me", response_model=Customer)
def get_me(customer_id: int = Depends(get_current_customer_id)):
    return database.customers[customer_id]
