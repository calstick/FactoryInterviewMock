from app.services import pricing

# NOTE (ISSUE-04): there is intentionally NO coverage of calculate_tax() here.
# That gap is the subject of the seeded "missing test coverage" ticket.


def test_no_discount_for_small_quantity():
    gross, discount = pricing.price_line(100.0, 5)
    assert gross == 500.0
    assert discount == 0.0


def test_bulk_discount_for_large_quantity():
    gross, discount = pricing.price_line(100.0, 15)
    assert gross == 1500.0
    assert discount == 150.0


def test_bulk_discount_threshold_boundary():
    assert pricing.price_line(19.99, 9) == (179.91, 0.0)
    assert pricing.price_line(19.99, 10) == (199.9, 19.99)
    assert pricing.price_line(19.99, 11) == (219.89, 21.99)


def test_price_order_aggregates_lines():
    line_inputs = [
        {"product": {"id": 1, "name": "A", "price": 50.0}, "quantity": 2},
        {"product": {"id": 2, "name": "B", "price": 20.0}, "quantity": 1},
    ]
    priced = pricing.price_order(line_inputs)
    assert priced["subtotal"] == 120.0
    assert priced["discount"] == 0.0
    assert len(priced["items"]) == 2
