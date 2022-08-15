def test_categoria(client):
    response = client.get("/categoria")
    assert response.status_code == 200


def test_categoria_id(client):
    response = client.get("/categoria?category_id=2")
    assert response.status_code == 200
    assert response.json()["data"] == {
        "id": 2,
        "name": "Categoria 2",
        "description": "descrição 2",
        "active": True,
        "updated_at": "2021-02-26T00:00:00",
    }


def test_categoria_id_not_found(client):
    response = client.get("/categoria?category_id=12")
    assert response.status_code == 200
    assert response.json()["message"] == "Nenhuma categoria encontrada"
