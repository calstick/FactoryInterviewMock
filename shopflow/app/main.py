import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers import auth as auth_router
from app.routers import cart, customers, orders, products

app = FastAPI(
    title="ShopFlow API",
    description="Order-management API for Riverbend Outfitters (demo).",
    version="0.1.0",
)

app.include_router(auth_router.router)
app.include_router(products.router)
app.include_router(cart.router)
app.include_router(orders.router)
app.include_router(customers.router)


@app.get("/health", tags=["system"])
def health():
    return {"status": "ok"}


FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.isdir(FRONTEND_DIR):
    app.mount("/app", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
