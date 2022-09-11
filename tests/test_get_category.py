from fastapi.testclient import TestClient
from utils.auth_utils import ADMIN_HEADER, BASIC_HEADER, MANAGER_HEADER


def test_get_categoria_as_admin(client: TestClient):
    response = client.get("/categoria", headers=ADMIN_HEADER)
    assert response.status_code == 200
    assert len(response.json()["data"]) == 9


def test_get_categoria_by_id_as_admin(client: TestClient):
    response = client.get("/categoria?category_id=2", headers=ADMIN_HEADER)
    assert response.status_code == 200
    assert response.json()["data"] == {
        "id": 2,
        "name": "Categoria 2",
        "description": "descrição 2",
        "active": True,
        "updated_at": "2021-02-26T00:00:00",
    }


def test_categoria_id_not_found_as_admin(client: TestClient):
    response = client.get("/categoria?category_id=12", headers=ADMIN_HEADER)
    assert response.status_code == 200
    assert response.json()["message"] == "Nenhuma categoria encontrada"


def test_get_categoria_as_manager(client: TestClient):
    response = client.get("/categoria", headers=MANAGER_HEADER)
    assert response.status_code == 200
    assert len(response.json()["data"]) == 9


def test_get_categoria_as_basic(client: TestClient):
    response = client.get("/categoria", headers=BASIC_HEADER)
    assert response.status_code == 200
    assert len(response.json()["data"]) == 9


def test_get_categoria_as_public(client: TestClient):
    response = client.get("/categoria")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 9
