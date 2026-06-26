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


def test_get_order_requires_auth(client, auth_headers):
    created = client.post(
        "/orders",
        json={"items": [{"product_id": 1, "quantity": 1}]},
        headers=auth_headers,
    )
    order_id = created.json()["id"]

    res = client.get(f"/orders/{order_id}")

    assert res.status_code == 401


def test_get_order_owner_can_fetch(client, auth_headers):
    created = client.post(
        "/orders",
        json={"items": [{"product_id": 1, "quantity": 1}]},
        headers=auth_headers,
    )
    order_id = created.json()["id"]

    res = client.get(f"/orders/{order_id}", headers=auth_headers)

    assert res.status_code == 200
    order = res.json()
    assert order["id"] == order_id
    assert order["customer_id"] == 101


def test_get_order_other_customer_not_found(client, auth_headers):
    created = client.post(
        "/orders",
        json={"items": [{"product_id": 1, "quantity": 1}]},
        headers=auth_headers,
    )
    order_id = created.json()["id"]
    login = client.post(
        "/auth/login",
        json={"email": "miguel@example.com", "password": "summit2024"},
    )
    other_headers = {"Authorization": f"Bearer {login.json()['token']}"}

    res = client.get(f"/orders/{order_id}", headers=other_headers)

    assert res.status_code == 404
