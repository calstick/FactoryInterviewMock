title: Missing test coverage for tax calculation and discount boundary
labels: tests, pricing
---

## Problem / motivation
`pricing.calculate_tax()` and the bulk-discount quantity boundary have no unit
tests. Pricing is revenue-critical; regressions here are expensive and currently
nothing would catch them in CI.

## Proposed solution
Add focused unit tests in `tests/test_pricing.py`:
- `calculate_tax()` for representative amounts (0, typical, rounding edge).
- `price_order()` end-to-end totals: subtotal, discount, tax, total.
- The bulk-discount boundary (quantities 9, 10, 11).

## Pointers
- `app/services/pricing.py`, `tests/test_pricing.py`.

## Acceptance criteria
- [ ] Tax calculation is covered for multiple amounts including a rounding case.
- [ ] `price_order()` total math is asserted end-to-end.
- [ ] Boundary tests exist for the bulk-discount threshold.

> Note: the boundary tests will surface ISSUE-01; coordinate the fix.
