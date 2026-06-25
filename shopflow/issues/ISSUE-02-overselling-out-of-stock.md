title: Orders accepted for more units than are in stock (overselling)
labels: bug, inventory
---

## Summary
The order endpoint accepts any quantity as long as stock is greater than zero. A
customer can order 50 units of an item that has only 3 in stock, driving
inventory negative and creating fulfillment problems.

## Steps to reproduce
1. Sign in.
2. `POST /orders` with `{"items": [{"product_id": 6, "quantity": 50}]}`
   (product 6 has stock 3).
3. Order is created (201) and stock goes negative.

## Expected behavior
An order line is only accepted when the requested quantity is **available**.
Requesting more than the available stock returns `409 Conflict`.

## Actual behavior
`is_in_stock()` only checks `stock > 0` and ignores the requested quantity, so
oversell orders succeed.

## Pointers
- `app/services/inventory.py` → `is_in_stock(product, quantity)`.

## Acceptance criteria
- [ ] Ordering more than available stock returns 409 and does not mutate stock.
- [ ] Ordering up to available stock still succeeds.
- [ ] Add regression tests for the boundary (qty == stock, qty == stock + 1).
