def test_login_success(client):
    res = client.post(
        "/auth/login", json={"email": "dana@example.com", "password": "trailmix1"}
    )
    assert res.status_code == 200
    body = res.json()
    assert body["customer_id"] == 101
    assert body["token"]


def test_login_wrong_password(client):
    res = client.post(
        "/auth/login", json={"email": "dana@example.com", "password": "wrong"}
    )
    assert res.status_code == 401


def test_me_requires_token(client):
    res = client.get("/customers/me")
    assert res.status_code == 401


def test_me_returns_current_customer(client, auth_headers):
    res = client.get("/customers/me", headers=auth_headers)
    assert res.status_code == 200
    assert res.json()["email"] == "dana@example.com"
