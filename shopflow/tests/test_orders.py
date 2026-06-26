from datetime import datetime, timezone

from app import database


def _auth_headers_for(client, email, password):
    res = client.post("/auth/login", json={"email": email, "password": password})
    token = res.json()["token"]
    return {"Authorization": f"Bearer {token}"}


def _place_order(client, headers):
    res = client.post(
        "/orders",
        json={"items": [{"product_id": 3, "quantity": 1}]},
        headers=headers,
    )
    assert res.status_code == 201
    return res.json()["id"]


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


def test_list_orders_filters_by_status(client, auth_headers):
    order_id = _place_order(client, auth_headers)

    pending_res = client.get(
        "/orders", params={"status": "pending"}, headers=auth_headers
    )
    shipped_res = client.get(
        "/orders", params={"status": "shipped"}, headers=auth_headers
    )

    assert pending_res.status_code == 200
    assert [order["id"] for order in pending_res.json()] == [order_id]
    assert shipped_res.status_code == 200
    assert shipped_res.json() == []


def test_list_orders_filters_by_inclusive_date_range(client, auth_headers):
    first_id = _place_order(client, auth_headers)
    second_id = _place_order(client, auth_headers)
    outside_id = _place_order(client, auth_headers)

    database.orders[first_id]["created_at"] = datetime(
        2024, 1, 10, 23, 59, tzinfo=timezone.utc
    )
    database.orders[second_id]["created_at"] = datetime(
        2024, 1, 15, 0, 1, tzinfo=timezone.utc
    )
    database.orders[outside_id]["created_at"] = datetime(
        2024, 1, 16, 0, 0, tzinfo=timezone.utc
    )

    res = client.get(
        "/orders",
        params={"start_date": "2024-01-10", "end_date": "2024-01-15"},
        headers=auth_headers,
    )

    assert res.status_code == 200
    assert [order["id"] for order in res.json()] == [first_id, second_id]


def test_list_orders_rejects_invalid_status(client, auth_headers):
    res = client.get("/orders", params={"status": "bogus"}, headers=auth_headers)

    assert res.status_code == 422


def test_list_orders_combines_filters_and_stays_customer_scoped(
    client, auth_headers
):
    miguel_headers = _auth_headers_for(
        client, "miguel@example.com", "summit2024"
    )
    matching_id = _place_order(client, auth_headers)
    wrong_status_id = _place_order(client, auth_headers)
    wrong_date_id = _place_order(client, auth_headers)
    other_customer_id = _place_order(client, miguel_headers)

    database.orders[matching_id].update(
        {
            "status": "shipped",
            "created_at": datetime(2024, 1, 15, 12, 0, tzinfo=timezone.utc),
        }
    )
    database.orders[wrong_status_id].update(
        {
            "status": "pending",
            "created_at": datetime(2024, 1, 15, 12, 0, tzinfo=timezone.utc),
        }
    )
    database.orders[wrong_date_id].update(
        {
            "status": "shipped",
            "created_at": datetime(2024, 1, 16, 12, 0, tzinfo=timezone.utc),
        }
    )
    database.orders[other_customer_id].update(
        {
            "status": "shipped",
            "created_at": datetime(2024, 1, 15, 12, 0, tzinfo=timezone.utc),
        }
    )

    res = client.get(
        "/orders",
        params={
            "status": "shipped",
            "start_date": "2024-01-15",
            "end_date": "2024-01-15",
        },
        headers=auth_headers,
    )

    assert res.status_code == 200
    assert [order["id"] for order in res.json()] == [matching_id]
