"""Minimal token-based auth for the demo.

A successful login returns an opaque token that maps back to a customer id.
Real deployments would use hashed passwords + signed tokens; this is kept
deliberately small for the demo.
"""

import secrets
from typing import Optional

from fastapi import Header, HTTPException, status

from app import database

# token -> customer_id
_sessions: dict = {}


def authenticate(email: str, password: str) -> Optional[int]:
    record = database.credentials.get(email)
    if not record or record["password"] != password:
        return None
    return record["customer_id"]


def issue_token(customer_id: int) -> str:
    token = secrets.token_hex(16)
    _sessions[token] = customer_id
    return token


def get_current_customer_id(authorization: Optional[str] = Header(default=None)) -> int:
    """FastAPI dependency: resolve the authenticated customer from the header."""
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or malformed Authorization header",
        )
    token = authorization.split(" ", 1)[1].strip()
    customer_id = _sessions.get(token)
    if customer_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    return customer_id
