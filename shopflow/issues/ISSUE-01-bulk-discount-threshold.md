title: Bulk discount not applied at the exact quantity threshold
labels: bug, pricing
---

## Summary
Customers who order exactly the bulk-discount threshold quantity (10 units) are
charged full price. The discount only kicks in at 11+, so the most common "round
number" bulk order silently misses the promised 10% line discount.

## Steps to reproduce
1. Add 10 units of a single product to the cart (e.g. product 3 at $19.99).
2. Call `POST /cart/preview` or place the order.
3. Observe `discount` is `0.0`.

## Expected behavior
A line quantity of **10 or more** receives the 10% bulk discount
(`BULK_DISCOUNT_RATE`).

## Actual behavior
Only quantities **strictly greater than 10** are discounted. Quantity 10 gets no
discount.

## Pointers
- `app/services/pricing.py` → `price_line()` uses `quantity > BULK_DISCOUNT_THRESHOLD`.

## Acceptance criteria
- [ ] Quantity == 10 receives the bulk discount.
- [ ] Quantity == 9 still receives no discount.
- [ ] Add a regression test covering the threshold boundary (9, 10, 11).
