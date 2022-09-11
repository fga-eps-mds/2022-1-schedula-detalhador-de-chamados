from fastapi.testclient import TestClient
from utils.auth_utils import ADMIN_HEADER, BASIC_HEADER, MANAGER_HEADER

problem = {"name": "test", "description": "test", "category_id": 1}


def test_put_problem_as_admin(client: TestClient):
    response = client.put(
        "/problema/1",
        json=problem,
        headers=ADMIN_HEADER
    )
    assert response.status_code == 200
    verify = client.get("/problema?problem_id=1")
    assert verify.json()["data"]["name"] == "test"


def test_put_problem_invalid_name_as_admin(client: TestClient):
    problem["name"] = None
    response = client.put(
        "/problema/1",
        json=problem,
        headers=ADMIN_HEADER
    )
    assert response.status_code == 422


def test_put_invalid_problem_as_admin(client: TestClient):
    problem["name"] = "Teste"
    response = client.put(
        "/problema/9999",
        json=problem,
        headers=ADMIN_HEADER
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Problema não encontrado"


def test_put_invalid_problem_category_as_admin(client: TestClient):
    problem["category_id"] = 90
    response = client.put(
        "/problema/2",
        json=problem,
        headers=ADMIN_HEADER
    )
    assert response.status_code == 400
    assert response.json()["message"] == "Categoria de problema invalida."


def test_put_problem_as_manager(client: TestClient):
    problem["category_id"] = 5
    problem["name"] = "test"
    response = client.put(
        "/problema/2",
        json=problem,
        headers=MANAGER_HEADER
    )
    assert response.status_code == 200
    verify = client.get("/problema?problem_id=2")
    assert verify.json()["data"]["name"] == "test"


def test_put_problem_as_basic(client: TestClient):
    response = client.put(
        "/problema/2",
        json=problem,
        headers=BASIC_HEADER
    )
    assert response.status_code == 401
    assert response.json()["message"] == "Acesso negado"


def test_put_problem_as_public(client: TestClient):
    response = client.put(
        "/problema/2",
        json=problem
    )
    assert response.status_code == 401
    assert response.json()["message"] == "Acesso negado"
