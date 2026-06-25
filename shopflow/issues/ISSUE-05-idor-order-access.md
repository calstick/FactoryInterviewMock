title: Security: any caller can read any customer's order (IDOR)
labels: security, orders
---

## Summary
`GET /orders/{order_id}` has no authentication and no ownership check. Anyone can
enumerate order ids and read another customer's order, including line items and
totals. This is an Insecure Direct Object Reference (IDOR) and a data-exposure
risk.

## Steps to reproduce
1. Customer A (id 101) places an order — it gets id 1.
2. Without any token (or as customer B), call `GET /orders/1`.
3. The full order is returned (200).

## Expected behavior
- The endpoint requires authentication.
- A customer may only read their **own** orders. Requesting another customer's
  order returns `404` (preferred, to avoid leaking existence) or `403`.

## Pointers
- `app/routers/orders.py` → `get_order()` (no `Depends(get_current_customer_id)`).
- Compare with `list_orders()`, which already scopes by `customer_id`.

## Acceptance criteria
- [ ] Unauthenticated request returns 401.
- [ ] Authenticated request for another customer's order returns 404/403.
- [ ] Owner can still fetch their own order.
- [ ] Add regression tests for all three cases.
