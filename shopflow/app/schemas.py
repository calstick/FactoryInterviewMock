"""Pydantic models used across the API for validation and serialization."""

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, EmailStr


class OrderStatus(str, Enum):
    pending = "pending"
    paid = "paid"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"


class Product(BaseModel):
    id: int
    name: str
    price: float
    stock: int
    category: str


class Customer(BaseModel):
    id: int
    name: str
    email: EmailStr


class CartItem(BaseModel):
    product_id: int
    quantity: int


class OrderItem(BaseModel):
    product_id: int
    name: str
    unit_price: float
    quantity: int
    line_total: float


class Order(BaseModel):
    id: int
    customer_id: int
    items: List[OrderItem]
    subtotal: float
    discount: float
    tax: float
    total: float
    status: OrderStatus
    created_at: datetime


class PlaceOrderRequest(BaseModel):
    items: List[CartItem]


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    token: str
    customer_id: int
    name: str
