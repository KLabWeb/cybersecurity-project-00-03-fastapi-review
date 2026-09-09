from fastapi import Response
from fastapi.testclient import TestClient

from api.dependencies.header import get_secret_header
from main import app

client = TestClient(app)


# Stand-in for get_secret_header
# Assume this is another secret header service provider we are testing before implementing
async def override_get_secret_header(response: Response) -> None:
    response.headers["secret"] = "New secret header"

def test_get_item():
    response = client.get("/items/0")
    assert response.status_code == 200
    assert response.json() == {"item_id": 0, "item_name": "Apple", "query": None}


def test_get_item_with_query():
    response = client.get("/items/0", params={"q": "apple"})
    assert response.status_code == 200
    assert response.json() == {"item_id": 0, "item_name": "Apple", "query": "apple"}


def test_get_nonexistent_item():
    response = client.get("/items/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_get_item_query_too_short():
    response = client.get("/items/0", params={"q": "a"})
    assert response.status_code == 422


def test_get_items_respects_limit():
    response = client.get("/items/", params={"limit": 2})
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_compare_item_prices():
    response = client.get("/items/price-comparison", params={"item_id": [0, 2]})
    assert response.status_code == 200
    assert response.json()["greater_price_item_id"] == 2


def test_compare_item_prices_requires_two_ids():
    response = client.get("/items/price-comparison", params={"item_id": [0]})
    assert response.status_code == 422

app.dependency_overrides[get_secret_header] = override_get_secret_header

def test_overriden_get_secret_header():
    response = client.get("items/0")
    assert response.status_code == 200
    assert response.headers["secret"] == "New secret header"
