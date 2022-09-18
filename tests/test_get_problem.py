from fastapi.testclient import TestClient

from utils.auth_utils import ADMIN_HEADER, BASIC_HEADER, MANAGER_HEADER


def test_get_problem_as_admin(client: TestClient):
    url = "/problema"
    response = client.get(url, headers=ADMIN_HEADER)
    assert response.status_code == 200
    assert response.json()["message"] == "Dados buscados com sucesso"
    assert len(response.json()["data"]) == 9


def test_get_problem_by_id_as_admin(client: TestClient):
    url = "/problema?id=1"
    response = client.get(url)
    assert response.status_code == 200


def test_get_problem_by_category_id(client: TestClient):
    url = "/problema?category_id=2"
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.json()["data"]) == 4


def test_get_problem_as_manager(client: TestClient):
    url = "/problema"
    response = client.get(url, headers=MANAGER_HEADER)
    assert response.status_code == 200
    assert response.json()["message"] == "Dados buscados com sucesso"
    assert len(response.json()["data"]) == 9


def test_get_problem_as_basic(client: TestClient):
    url = "/problema"
    response = client.get(url, headers=BASIC_HEADER)
    assert response.status_code == 200
    assert response.json()["message"] == "Dados buscados com sucesso"
    assert len(response.json()["data"]) == 9


def test_get_problem_as_public(client: TestClient):
    url = "/problema"
    response = client.get(url)
    assert response.status_code == 200
    assert response.json()["message"] == "Dados buscados com sucesso"
    assert len(response.json()["data"]) == 9
