def test_delete_request(client):
    response = client.delete("/chamado?request_id=1&problem_id=1")
    assert response.status_code == 200
    assert response.json()["message"] == "Chamado marcado como resolvido"
    assert response.json()["data"]["request_status"] == "solved"


def test_delete_invalid_request(client):
    response = client.delete("/chamado?request_id=99&problem_id=99")
    assert response.status_code == 200
    assert response.json()["message"] == "Chamado não encontrado"


def test_delete_request_without_problem_id(client):
    response = client.delete("/chamado?request_id=1")
    assert response.status_code == 422


def test_delete_request_without_request_id(client):
    response = client.delete("/chamado?problem_id=1")
    assert response.status_code == 422


def test_delete_request_without_request_id_and_problem_id(client):
    response = client.delete("/chamado")
    assert response.status_code == 422


def test_delete_request_with_invalid_request_id(client):
    response = client.delete("/chamado?request_id=abc&problem_id=1")
    assert response.status_code == 422


def test_delete_request_with_invalid_problem_id(client):
    response = client.delete("/chamado?request_id=1&problem_id=abc")
    assert response.status_code == 422


def test_delete_request_with_invalid_request_id_and_problem_id(client):
    response = client.delete("/chamado?request_id=abc&problem_id=abc")
    assert response.status_code == 422
