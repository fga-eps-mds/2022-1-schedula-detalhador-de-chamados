from fastapi.testclient import TestClient
from utils.auth_utils import ADMIN_HEADER, BASIC_HEADER, MANAGER_HEADER

category = {"name": "test", "description": "test"}


def test_post_category_as_admin(client: TestClient):
    response = client.post(
        "/categoria",
        json=category,
        headers=ADMIN_HEADER
    )
    assert response.status_code == 201


def test_post_category_invalid_name_as_admin(client: TestClient):
    response = client.post(
        "/categoria",
        json={"name": None, "description": "test"},
        headers=ADMIN_HEADER
    )
    assert response.status_code == 422


def test_post_category_as_manager(client: TestClient):
    response = client.post(
        "/categoria",
        json=category,
        headers=MANAGER_HEADER
    )
    assert response.status_code == 201


def test_post_category_as_basic(client: TestClient):
    response = client.post(
        "/categoria",
        json=category,
        headers=BASIC_HEADER
    )
    assert response.status_code == 401
    assert response.json()["message"] == "Acesso negado"


def test_post_category_as_public(client: TestClient):
    response = client.post(
        "/categoria",
        json=category
    )
    assert response.status_code == 401
    assert response.json()["message"] == "Acesso negado"
