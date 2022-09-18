from fastapi.testclient import TestClient

from utils.auth_utils import ADMIN_HEADER, BASIC_HEADER, MANAGER_HEADER


def test_delete_request_as_admin(client: TestClient):
    response = client.delete(
        "/chamado?request_id=1&problem_id=1", headers=ADMIN_HEADER)
    assert response.status_code == 200
    assert response.json()["message"] == "Chamado marcado como resolvido"
    assert response.json()["data"]["request_status"] == "solved"


def test_delete_invalid_request_as_admin(client: TestClient):
    response = client.delete(
        "/chamado?request_id=99&problem_id=99", headers=ADMIN_HEADER)
    assert response.status_code == 200
    assert response.json()["message"] == "Chamado não encontrado"


def test_delete_request_without_problem_id_as_admin(client: TestClient):
    response = client.delete("/chamado?request_id=1", headers=ADMIN_HEADER)
    assert response.status_code == 422


def test_delete_request_without_request_id_as_admin(client: TestClient):
    response = client.delete("/chamado?problem_id=1", headers=ADMIN_HEADER)
    assert response.status_code == 422


def test_delete_request_without_request_id_and_problem_id_as_admin(client: TestClient):  # noqa 501
    response = client.delete("/chamado", headers=ADMIN_HEADER)
    assert response.status_code == 422


def test_delete_request_with_invalid_request_id_as_admin(client: TestClient):
    response = client.delete(
        "/chamado?request_id=abc&problem_id=1", headers=ADMIN_HEADER)
    assert response.status_code == 422


def test_delete_request_with_invalid_problem_id_as_admin(client: TestClient):
    response = client.delete(
        "/chamado?request_id=1&problem_id=abc", headers=ADMIN_HEADER)
    assert response.status_code == 422


def test_delete_request_with_invalid_request_id_and_problem_id_as_admin(client: TestClient):  # noqa 501
    response = client.delete(
        "/chamado?request_id=abc&problem_id=abc", headers=ADMIN_HEADER)
    assert response.status_code == 422


def test_delete_request_as_manager(client: TestClient):
    response = client.delete(
        "/chamado?request_id=1&problem_id=1", headers=MANAGER_HEADER)
    assert response.status_code == 401
    assert response.json()["message"] == "Acesso negado"


def test_delete_request_as_basic(client: TestClient):
    response = client.delete(
        "/chamado?request_id=1&problem_id=1", headers=BASIC_HEADER)
    assert response.status_code == 401
    assert response.json()["message"] == "Acesso negado"


def test_delete_request_as_public(client: TestClient):
    response = client.delete(
        "/chamado?request_id=1&problem_id=1")
    assert response.status_code == 401
    assert response.json()["message"] == "Acesso negado"
