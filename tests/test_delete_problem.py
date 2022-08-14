def test_delete_problem(client):
    response = client.delete("/problema/1")
    assert response.status_code == 200


def test_delete_invalid_problem(client):
    response = client.delete("/problema/99")
    assert response.status_code == 200
    assert response.json()["message"] == "Problema de id: 99 não encontrado"
