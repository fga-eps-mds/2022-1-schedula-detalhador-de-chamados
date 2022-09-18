from fastapi.testclient import TestClient

from utils.auth_utils import ADMIN_HEADER, BASIC_HEADER, MANAGER_HEADER


def test_delete_category_as_admin(client: TestClient):
    response = client.delete("/categoria/10", headers=ADMIN_HEADER)
    assert response.status_code == 200
    assert (
        response.json()["message"]
        == "Categoria de id = 10 deletada com sucesso"
    )
    verify = client.get("/categoria?category_id=10")
    assert verify.status_code == 200
    assert not verify.json()["data"]["active"]


def test_delete_category_not_found_as_admin(client: TestClient):
    response = client.delete("/categoria/12", headers=ADMIN_HEADER)
    assert response.status_code == 200
    assert response.json()["message"] == "Categoria de id = 12 não encontrada"


def test_delete_category_as_manager(client: TestClient):
    response = client.delete("/categoria/10", headers=MANAGER_HEADER)
    assert response.status_code == 401
    assert response.json()["message"] == "Acesso negado"


def test_delete_category_as_basic(client: TestClient):
    response = client.delete("/categoria/10", headers=BASIC_HEADER)
    assert response.status_code == 401
    assert response.json()["message"] == "Acesso negado"


def test_delete_category_as_public(client: TestClient):
    response = client.delete("/categoria/10")
    assert response.status_code == 401
    assert response.json()["message"] == "Acesso negado"
