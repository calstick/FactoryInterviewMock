import pytest

from app.services import pricing


def test_no_discount_for_small_quantity():
    gross, discount = pricing.price_line(100.0, 5)
    assert gross == 500.0
    assert discount == 0.0


def test_bulk_discount_for_large_quantity():
    gross, discount = pricing.price_line(100.0, 15)
    assert gross == 1500.0
    assert discount == 150.0


@pytest.mark.parametrize(
    ("amount", "expected_tax"),
    [
        (0.0, 0.0),
        (125.0, 10.0),
        (19.99, 1.6),
    ],
)
def test_calculate_tax_for_representative_amounts(amount, expected_tax):
    assert pricing.calculate_tax(amount) == expected_tax


def test_price_order_aggregates_lines():
    line_inputs = [
        {"product": {"id": 1, "name": "A", "price": 50.0}, "quantity": 2},
        {"product": {"id": 2, "name": "B", "price": 20.0}, "quantity": 1},
    ]
    priced = pricing.price_order(line_inputs)
    assert priced["subtotal"] == 120.0
    assert priced["discount"] == 0.0
    assert len(priced["items"]) == 2


def test_price_order_calculates_end_to_end_totals():
    line_inputs = [
        {
            "product": {"id": 3, "name": "Riverbend Water Bottle", "price": 19.99},
            "quantity": 10,
        },
        {
            "product": {"id": 6, "name": "Trail Running Socks (3-pack)", "price": 24.99},
            "quantity": 2,
        },
    ]

    priced = pricing.price_order(line_inputs)

    assert priced["subtotal"] == 249.88
    assert priced["discount"] == 19.99
    assert priced["tax"] == 18.39
    assert priced["total"] == 248.28
    assert priced["items"][0].line_total == 179.91
    assert priced["items"][1].line_total == 49.98


@pytest.mark.parametrize(
    ("quantity", "expected_discount"),
    [
        (9, 0.0),
        (10, 19.99),
        (11, 21.99),
    ],
)
def test_bulk_discount_boundary_for_quantities_9_10_11(quantity, expected_discount):
    gross, discount = pricing.price_line(19.99, quantity)

    assert gross == round(19.99 * quantity, 2)
    assert discount == expected_discount
