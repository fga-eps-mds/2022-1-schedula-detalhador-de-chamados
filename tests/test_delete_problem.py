from fastapi.testclient import TestClient

from utils.auth_utils import ADMIN_HEADER, BASIC_HEADER, MANAGER_HEADER


def test_delete_problem_as_admin(client: TestClient):
    response = client.delete("/problema/1", headers=ADMIN_HEADER)
    assert response.status_code == 200
    verify = client.get("/problema?problem_id=1")
    assert not verify.json()["data"]["active"]


def test_delete_invalid_problem_as_admin(client: TestClient):
    response = client.delete("/problema/99", headers=ADMIN_HEADER)
    assert response.status_code == 200
    assert response.json()["message"] == "Problema de id: 99 não encontrado"


def test_delete_problem_as_manager(client: TestClient):
    response = client.delete("/problema/1", headers=MANAGER_HEADER)
    assert response.status_code == 401
    assert response.json()["message"] == "Acesso negado"


def test_delete_problem_as_basic(client: TestClient):
    response = client.delete("/problema/1", headers=BASIC_HEADER)
    assert response.status_code == 401
    assert response.json()["message"] == "Acesso negado"


def test_delete_problem_as_public(client: TestClient):
    response = client.delete("/problema/1")
    assert response.status_code == 401
    assert response.json()["message"] == "Acesso negado"
