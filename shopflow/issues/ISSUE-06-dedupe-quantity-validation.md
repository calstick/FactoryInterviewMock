title: Refactor: deduplicate quantity validation and remove magic numbers
labels: tech-debt, refactor
---

## Problem / motivation
Quantity validation (`1 <= quantity <= 99`) is re-implemented inline in multiple
routers with the literal `99`, while `app/utils/validation.py` already provides a
`validate_quantity()` helper backed by `config.MAX_LINE_QUANTITY`. The
duplication is error-prone — limits can drift between endpoints.

## Proposed solution
- Replace the inline checks in `app/routers/orders.py` and `app/routers/cart.py`
  with calls to `utils.validation.validate_quantity()`.
- Ensure the helper uses `config.MAX_LINE_QUANTITY` (no hard-coded literals).
- Confirm error responses remain 422.

## Pointers
- `app/routers/orders.py`, `app/routers/cart.py`, `app/utils/validation.py`,
  `app/config.py`.

## Acceptance criteria
- [ ] No remaining inline `quantity > 99` literals in routers.
- [ ] Both endpoints call the shared helper.
- [ ] Existing behavior preserved (422 on invalid quantity); tests still green.
