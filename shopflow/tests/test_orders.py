def test_place_order_requires_auth(client):
    res = client.post("/orders", json={"items": [{"product_id": 1, "quantity": 1}]})
    assert res.status_code == 401


def test_place_order_succeeds(client, auth_headers):
    res = client.post(
        "/orders",
        json={"items": [{"product_id": 1, "quantity": 2}]},
        headers=auth_headers,
    )
    assert res.status_code == 201
    order = res.json()
    assert order["subtotal"] == 259.98
    assert order["discount"] == 0.0
    assert order["total"] == 280.78
    assert order["status"] == "pending"


def test_place_order_reduces_stock(client, auth_headers):
    client.post(
        "/orders",
        json={"items": [{"product_id": 3, "quantity": 5}]},
        headers=auth_headers,
    )
    res = client.get("/products/3")
    assert res.json()["stock"] == 195


def test_place_order_allows_quantity_equal_to_stock(client, auth_headers):
    res = client.post(
        "/orders",
        json={"items": [{"product_id": 6, "quantity": 3}]},
        headers=auth_headers,
    )
    assert res.status_code == 201

    stock_res = client.get("/products/6")
    assert stock_res.json()["stock"] == 0


def test_place_order_rejects_quantity_above_stock_without_mutating_stock(
    client, auth_headers
):
    res = client.post(
        "/orders",
        json={"items": [{"product_id": 6, "quantity": 4}]},
        headers=auth_headers,
    )
    assert res.status_code == 409

    stock_res = client.get("/products/6")
    assert stock_res.json()["stock"] == 3


def test_place_order_rejects_empty(client, auth_headers):
    res = client.post("/orders", json={"items": []}, headers=auth_headers)
    assert res.status_code == 422


def test_list_orders_scoped_to_customer(client, auth_headers):
    client.post(
        "/orders",
        json={"items": [{"product_id": 1, "quantity": 1}]},
        headers=auth_headers,
    )
    res = client.get("/orders", headers=auth_headers)
    assert res.status_code == 200
    orders = res.json()
    assert len(orders) == 1
    assert orders[0]["customer_id"] == 101
