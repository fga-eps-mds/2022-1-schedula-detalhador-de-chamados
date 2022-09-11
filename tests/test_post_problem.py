from fastapi.testclient import TestClient
from utils.auth_utils import ADMIN_HEADER, BASIC_HEADER, MANAGER_HEADER

problem = {"name": "test", "description": "test", "category_id": 1}


def test_post_problem_as_admin(client: TestClient):
    response = client.post(
        "/problema",
        json=problem,
        headers=ADMIN_HEADER
    )
    assert response.status_code == 201


def test_post_problem_invalid_as_admin(client: TestClient):
    problem['name'] = None
    response = client.post(
        "/problema",
        json=problem,
        headers=ADMIN_HEADER
    )
    assert response.status_code == 422


def test_post_problem_invalid_category_as_admin(client: TestClient):
    problem['name'] = "Teste"
    problem['category_id'] = 90
    response = client.post(
        "/problema",
        json=problem,
        headers=ADMIN_HEADER
    )
    assert response.status_code == 400
    assert response.json()["message"] == "Categoria de problema invalida."


def test_post_problem_as_manager(client: TestClient):
    problem['name'] = "Teste"
    problem['category_id'] = 2
    response = client.post(
        "/problema",
        json=problem,
        headers=MANAGER_HEADER
    )
    assert response.status_code == 201


def test_post_problem_as_basic(client: TestClient):
    response = client.post(
        "/problema",
        json=problem,
        headers=BASIC_HEADER
    )
    assert response.status_code == 401
    assert response.json()["message"] == "Acesso negado"


def test_post_problem_as_public(client: TestClient):
    response = client.post(
        "/problema",
        json=problem,
    )
    assert response.status_code == 401
    assert response.json()["message"] == "Acesso negado"
