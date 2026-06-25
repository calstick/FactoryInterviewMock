title: Add filtering of orders by status and date range
labels: enhancement, orders
---

## Problem / motivation
Support and ops need to find orders by status (e.g. all `pending`) and within a
date window when handling customer questions. Today `GET /orders` returns every
order for the customer with no way to narrow results.

## Proposed solution
Extend `GET /orders` with optional query parameters:
- `status`: one of the `OrderStatus` values.
- `start_date` / `end_date`: ISO dates; filter on `created_at` (inclusive).

Filters combine (logical AND). Omitting all params preserves current behavior.

## Pointers
- `app/routers/orders.py` → `list_orders()`.

## Acceptance criteria
- [ ] `?status=pending` returns only matching orders.
- [ ] `?start_date=...&end_date=...` filters by `created_at`.
- [ ] Invalid `status` returns 422.
- [ ] Add tests covering each filter and their combination.
