from pathlib import Path


ROUTERS_DIR = Path(__file__).resolve().parents[1] / "app" / "routers"


def test_quantity_validation_uses_shared_helper_without_magic_numbers():
    for router_file in ("orders.py", "cart.py"):
        source = (ROUTERS_DIR / router_file).read_text()
        assert "validate_quantity" in source
        assert "quantity > 99" not in source
        assert "> 99" not in source


def test_place_order_rejects_quantity_bounds(client, auth_headers):
    for quantity in (0, 100):
        res = client.post(
            "/orders",
            json={"items": [{"product_id": 1, "quantity": quantity}]},
            headers=auth_headers,
        )
        assert res.status_code == 422


def test_cart_preview_rejects_quantity_bounds(client):
    for quantity in (0, 100):
        res = client.post(
            "/cart/preview",
            json={"items": [{"product_id": 1, "quantity": quantity}]},
        )
        assert res.status_code == 422


def test_valid_quantities_still_work(client, auth_headers):
    order_res = client.post(
        "/orders",
        json={"items": [{"product_id": 1, "quantity": 2}]},
        headers=auth_headers,
    )
    assert order_res.status_code == 201

    preview_res = client.post(
        "/cart/preview",
        json={"items": [{"product_id": 1, "quantity": 2}]},
    )
    assert preview_res.status_code == 200
    assert preview_res.json()["total"] > 0
