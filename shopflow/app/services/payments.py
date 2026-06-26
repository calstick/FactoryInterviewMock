"""Simulated payment provider integrations."""

import hashlib
from typing import Optional


VALID_APPLE_PAY_TOKEN_PREFIX = "mock_apple_pay_"


def _is_valid_mock_token(token: Optional[str]) -> bool:
    """Return True when the token follows the demo Apple Pay token rule.

    A token is valid only when it is non-empty after trimming whitespace and
    starts with ``mock_apple_pay_`` followed by at least one additional character.
    """
    if token is None:
        return False
    normalized = token.strip()
    return normalized.startswith(VALID_APPLE_PAY_TOKEN_PREFIX) and (
        len(normalized) > len(VALID_APPLE_PAY_TOKEN_PREFIX)
    )


def process_apple_pay(amount: float, token: str) -> dict:
    """Authorize a simulated Apple Pay charge for ``amount``.

    The mock provider approves only tokens that satisfy the explicit rule in
    ``_is_valid_mock_token`` and declines empty or invalid tokens.
    """
    if not _is_valid_mock_token(token):
        return {"approved": False, "authorization_id": None, "reason": "invalid_token"}

    normalized = token.strip()
    digest = hashlib.sha256(f"{amount:.2f}:{normalized}".encode("utf-8")).hexdigest()
    return {
        "approved": True,
        "authorization_id": f"ap_mock_{digest[:12]}",
        "reason": None,
    }
