def login_headers(client, email, password):
    res = client.post("/auth/login", json={"email": email, "password": password})
    assert res.status_code == 200
    token = res.json()["token"]
    return {"Authorization": f"Bearer {token}"}


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
    assert order["payment_status"] == "unpaid"
    assert order["payment_method"] is None


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


def test_pay_order_with_valid_apple_pay_token_marks_order_paid(client, auth_headers):
    order_res = client.post(
        "/orders",
        json={"items": [{"product_id": 3, "quantity": 1}]},
        headers=auth_headers,
    )
    assert order_res.status_code == 201
    order_id = order_res.json()["id"]

    pay_res = client.post(
        f"/orders/{order_id}/pay",
        json={"token": "mock_apple_pay_success"},
        headers=auth_headers,
    )

    assert pay_res.status_code == 200
    paid_order = pay_res.json()
    assert paid_order["payment_status"] == "paid"
    assert paid_order["payment_method"] == "apple_pay"

    get_res = client.get(f"/orders/{order_id}")
    assert get_res.json()["payment_status"] == "paid"
    assert get_res.json()["payment_method"] == "apple_pay"


def test_pay_order_with_invalid_apple_pay_token_returns_402_and_stays_unpaid(
    client, auth_headers
):
    order_res = client.post(
        "/orders",
        json={"items": [{"product_id": 3, "quantity": 1}]},
        headers=auth_headers,
    )
    assert order_res.status_code == 201
    order_id = order_res.json()["id"]

    pay_res = client.post(
        f"/orders/{order_id}/pay",
        json={"token": "not-a-valid-mock-token"},
        headers=auth_headers,
    )

    assert pay_res.status_code == 402
    get_res = client.get(f"/orders/{order_id}")
    assert get_res.json()["payment_status"] == "unpaid"
    assert get_res.json()["payment_method"] is None


def test_pay_order_with_empty_apple_pay_token_returns_402_and_stays_unpaid(
    client, auth_headers
):
    order_res = client.post(
        "/orders",
        json={"items": [{"product_id": 3, "quantity": 1}]},
        headers=auth_headers,
    )
    assert order_res.status_code == 201
    order_id = order_res.json()["id"]

    pay_res = client.post(
        f"/orders/{order_id}/pay",
        json={"token": ""},
        headers=auth_headers,
    )

    assert pay_res.status_code == 402
    get_res = client.get(f"/orders/{order_id}")
    assert get_res.json()["payment_status"] == "unpaid"
    assert get_res.json()["payment_method"] is None


def test_pay_order_blocks_non_owner_and_keeps_order_unpaid(client, auth_headers):
    order_res = client.post(
        "/orders",
        json={"items": [{"product_id": 3, "quantity": 1}]},
        headers=auth_headers,
    )
    assert order_res.status_code == 201
    order_id = order_res.json()["id"]
    miguel_headers = login_headers(client, "miguel@example.com", "summit2024")

    pay_res = client.post(
        f"/orders/{order_id}/pay",
        json={"token": "mock_apple_pay_success"},
        headers=miguel_headers,
    )

    assert pay_res.status_code == 404
    get_res = client.get(f"/orders/{order_id}")
    assert get_res.json()["payment_status"] == "unpaid"
    assert get_res.json()["payment_method"] is None


def test_pay_order_requires_auth(client, auth_headers):
    order_res = client.post(
        "/orders",
        json={"items": [{"product_id": 3, "quantity": 1}]},
        headers=auth_headers,
    )
    assert order_res.status_code == 201
    order_id = order_res.json()["id"]

    pay_res = client.post(
        f"/orders/{order_id}/pay",
        json={"token": "mock_apple_pay_success"},
    )

    assert pay_res.status_code == 401
