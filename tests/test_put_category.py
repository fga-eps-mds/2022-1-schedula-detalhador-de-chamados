def test_put_category(client):
    response = client.put(
        "/categoria/1", json={"name": "test", "description": "test"}
    )
    assert response.status_code == 200


def test_put_category_invalid_name(client):
    response = client.put(
        "/categoria/1", json={"name": None, "description": "test"}
    )
    assert response.status_code == 422


def test_put_invalid_category(client):
    response = client.put(
        "/categoria/12", json={"name": "test", "description": "test"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Categoria não encontrada"
