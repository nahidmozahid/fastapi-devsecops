import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert "message" in r.json()


def test_list_items():
    r = client.get("/items/")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_get_existing_item():
    r = client.get("/items/1")
    assert r.status_code == 200
    assert r.json()["name"] == "apple"


def test_create_item_and_conflict():
    payload = {"id": 3, "name": "orange", "description": "citrus"}
    r = client.post("/items/", json=payload)
    assert r.status_code == 201
    # duplicate id should fail
    r2 = client.post("/items/", json=payload)
    assert r2.status_code == 400
