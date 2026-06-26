title: Add Apple Pay checkout (simulated)
labels: enhancement, payments, orders
---

## Problem / motivation
Customers expect one-tap wallet payments at checkout. Competitors already offer
Apple Pay, and the lack of an express payment option contributes to cart
abandonment and lost revenue. ShopFlow currently records orders as `pending`
with no way to capture payment.

## Proposed solution
Add a **simulated** Apple Pay payment flow (no real payment processor — a mock
provider that approves/declines based on a token), wired into the order
lifecycle. Keep existing `POST /orders` behavior unchanged (orders still start
`pending` / `unpaid`); payment is a separate, additive step.

- `app/services/payments.py`: `process_apple_pay(amount, token)` returning an
  authorization result — approved for a valid mock token, declined otherwise.
- New endpoint `POST /orders/{order_id}/pay` (authenticated, owner-only) that
  charges via the provider and, on success, sets the order's `payment_status`
  to `paid` and records `payment_method = "apple_pay"`.
- Extend the order schema with `payment_status` (default `unpaid`) and
  `payment_method` (default `null`).
- Frontend: a "Pay with Apple Pay" button shown after an order is placed; on
  success show "Paid with Apple Pay".

## Acceptance criteria
- [ ] `POST /orders/{id}/pay` with a valid mock Apple Pay token marks the order
      `paid` and `payment_method == "apple_pay"`.
- [ ] An invalid/empty token returns `402 Payment Required` and leaves the order
      unpaid.
- [ ] Only the order's owner can pay for it (auth + ownership check); others get
      404/403.
- [ ] Existing order placement is unchanged.
- [ ] Tests cover approved payment, declined payment, and ownership.

> Note: simulated for the demo. A production build would integrate a real
> payment service provider (e.g. Stripe / Apple Pay).
