"""Smoke tests for the generated FastAPI app (uses a temp database)."""
import os
import tempfile

_tmp = tempfile.mkdtemp()
os.environ["APP_DB_PATH"] = os.path.join(_tmp, "test.db")

from fastapi.testclient import TestClient  # noqa: E402
from app.main import app  # noqa: E402

client = TestClient(app)


def test_health():
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


def test_item_lifecycle():
    created = client.post("/api/items", json={"title": "Ship it"})
    assert created.status_code == 201
    body = created.json()
    assert body["title"] == "Ship it"
    assert body["completed"] is False

    listed = client.get("/api/items")
    assert listed.status_code == 200
    assert any(item["id"] == body["id"] for item in listed.json())

    updated = client.patch(f"/api/items/{body['id']}", json={"completed": True})
    assert updated.status_code == 200
    assert updated.json()["completed"] is True

    deleted = client.delete(f"/api/items/{body['id']}")
    assert deleted.status_code == 204


def test_create_validation():
    res = client.post("/api/items", json={"title": "   "})
    assert res.status_code == 422


def test_patch_missing_returns_404():
    res = client.patch("/api/items/999999", json={"completed": True})
    assert res.status_code == 404
