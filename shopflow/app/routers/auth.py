from fastapi import APIRouter, HTTPException, status

from app import auth, database
from app.schemas import LoginRequest, LoginResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
def login(req: LoginRequest):
    customer_id = auth.authenticate(req.email, req.password)
    if customer_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    token = auth.issue_token(customer_id)
    customer = database.customers[customer_id]
    return LoginResponse(token=token, customer_id=customer_id, name=customer["name"])
