def test_list_products(client):
    res = client.get("/products")
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 8
    assert {p["name"] for p in data}  # all have names


def test_filter_by_category(client):
    res = client.get("/products", params={"category": "outerwear"})
    assert res.status_code == 200
    data = res.json()
    assert all(p["category"] == "outerwear" for p in data)
    assert len(data) == 2


def test_get_single_product(client):
    res = client.get("/products/1")
    assert res.status_code == 200
    assert res.json()["name"] == "Trailhead Hiking Boots"


def test_get_missing_product(client):
    res = client.get("/products/9999")
    assert res.status_code == 404
