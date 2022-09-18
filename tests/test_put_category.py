from fastapi.testclient import TestClient

from utils.auth_utils import ADMIN_HEADER, BASIC_HEADER, MANAGER_HEADER

category = {"name": "test", "description": "test"}


def test_put_category_as_admin(client: TestClient):
    response = client.put(
        "/categoria/1",
        json=category,
        headers=ADMIN_HEADER
    )
    assert response.status_code == 200
    verify = client.get("/categoria?category_id=1")
    assert verify.json()["data"]["name"] == "test"
    assert verify.json()["data"]["description"] == "test"


def test_put_category_invalid_name_as_admin(client: TestClient):
    category["name"] = None
    response = client.put(
        "/categoria/1",
        json=category,
        headers=ADMIN_HEADER
    )
    assert response.status_code == 422


def test_put_invalid_category_as_admin(client: TestClient):
    category["name"] = "test"
    response = client.put(
        "/categoria/50",
        json=category,
        headers=ADMIN_HEADER
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Categoria não encontrada"


def test_put_category_as_manager(client: TestClient):
    response = client.put(
        "/categoria/2",
        json=category,
        headers=MANAGER_HEADER
    )
    assert response.status_code == 200
    verify = client.get("/categoria?category_id=2")
    assert verify.json()["data"]["name"] == "test"
    assert verify.json()["data"]["description"] == "test"


def test_put_category_as_basic(client: TestClient):
    response = client.put(
        "/categoria/3",
        json=category,
        headers=BASIC_HEADER
    )
    assert response.status_code == 401
    assert response.json()["message"] == "Acesso negado"
