def test_put_problem(client):
    response = client.put(
        "/problema/1",
        json={"name": "test", "description": "test", "category_id": 1},
    )
    assert response.status_code == 200


def test_put_problem_invalid_name(client):
    response = client.put(
        "/problema/1", json={"name": None, "description": "test"}
    )
    assert response.status_code == 422


# def test_put_invalid_problem(client):
#     response = client.put(
#         "/problema/9999", json={"name": "test", "description": "test"}
#     )
#     assert response.status_code == 200
#     assert response.json()["message"] == "Problema não encontrado"
