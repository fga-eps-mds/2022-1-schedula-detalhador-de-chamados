def test_post_problem(client):
    response = client.post(
        "/problema/",
        json={
            "name": "test",
            "description": "test",
            "category_id": 1})
    assert response.status_code == 201
    
    # assert response.json() == {
    #     "message": "Dados cadastrados com sucesso",
    #     "error": None,
    #     "data": {
    #         "id": 11,
    #         "name": "test",
    #         "description": "test",
    #         "active":True,
    #         # "updated_at": "2021-09-29T00:00:00",
    #         "category_id":1,
    #     }
    # }

def test_put_problem(client):
    response = client.put(
        "/problema/1",
        json={
            "name": "test",
            "description": "test",
            "category_id": 1})
    assert response.status_code == 200

def test_delete_problem(client):
    response = client.delete(
        "/problema/1")
    assert response.status_code == 200