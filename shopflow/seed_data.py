"""Seed data for the ShopFlow demo store (Riverbend Outfitters)."""

PRODUCTS = [
    {"id": 1, "name": "Trailhead Hiking Boots", "price": 129.99, "stock": 25, "category": "footwear"},
    {"id": 2, "name": "Summit Down Jacket", "price": 199.99, "stock": 12, "category": "outerwear"},
    {"id": 3, "name": "Riverbend Water Bottle", "price": 19.99, "stock": 200, "category": "accessories"},
    {"id": 4, "name": "Backcountry 45L Pack", "price": 159.99, "stock": 8, "category": "packs"},
    {"id": 5, "name": "Merino Base Layer", "price": 49.99, "stock": 60, "category": "apparel"},
    {"id": 6, "name": "Trail Running Socks (3-pack)", "price": 24.99, "stock": 3, "category": "apparel"},
    {"id": 7, "name": "Alpine Trekking Poles", "price": 89.99, "stock": 0, "category": "accessories"},
    {"id": 8, "name": "Stormproof Rain Shell", "price": 139.99, "stock": 18, "category": "outerwear"},
]

# Customer records plus plaintext demo passwords (demo only — not production auth).
CUSTOMERS = [
    {"id": 101, "name": "Dana Whitfield", "email": "dana@example.com", "password": "trailmix1"},
    {"id": 102, "name": "Miguel Ortega", "email": "miguel@example.com", "password": "summit2024"},
    {"id": 103, "name": "Priya Nair", "email": "priya@example.com", "password": "basecamp7"},
]
