def test_delete_category(client):
    response = client.delete("/categoria/10")
    assert response.status_code == 200
    assert (
        response.json()["message"]
        == "Categoria de id = 10 deletada com sucesso"
    )
    verify = client.get("/categoria/?category_id=10")
    assert verify.status_code == 200
    assert not verify.json()["data"]["active"]


def test_delete_category_not_found(client):
    response = client.delete("/categoria/12")
    assert response.status_code == 200
    assert response.json()["message"] == "Categoria de id = 12 não encontrada"
