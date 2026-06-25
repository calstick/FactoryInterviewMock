import os
import sys

import pytest
from fastapi.testclient import TestClient

# Ensure the project root is importable when running pytest from anywhere.
ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app import auth, database  # noqa: E402
from app.main import app  # noqa: E402


@pytest.fixture(autouse=True)
def reset_state():
    database.reset()
    auth._sessions.clear()
    yield


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def auth_headers(client):
    res = client.post(
        "/auth/login", json={"email": "dana@example.com", "password": "trailmix1"}
    )
    token = res.json()["token"]
    return {"Authorization": f"Bearer {token}"}
