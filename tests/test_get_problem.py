def test_get_problem(client):
    response = client.get("/problema/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "dados buscados com sucesso",
        "error": None,
        "data": [
            {"id": 1, "name": "Problema 1", "description": "descrição 1","active":True,"updated_at":"2021-02-26T00:00:00","category_id": 1},
            {"id": 2, "name": "Problema 2", "description": "descrição 2","active":True,"updated_at":"2021-02-26T00:00:00","category_id": 1},
            {"id": 3, "name": "Problema 3", "description": "descrição 3","active":True,"updated_at":"2021-12-26T00:00:00","category_id": 1},
            {"id": 4, "name": "Problema 4", "description": "descrição 4","active":True,"updated_at":"2021-11-26T00:00:00","category_id": 1},
            {"id": 5, "name": "Problema 5", "description": "descrição 5","active":True,"updated_at":"2021-10-26T00:00:00","category_id": 1},
            {"id": 6, "name": "Problema 6", "description": "descrição 6","active":True,"updated_at":"2021-09-26T00:00:00","category_id": 1},
            {"id": 7, "name": "Problema 7", "description": "descrição 7","active":True,"updated_at":"2021-06-26T00:00:00","category_id": 1},
            {"id": 8, "name": "Problema 8", "description": "descrição 8","active":True, "updated_at":"2021-05-26T00:00:00","category_id": 1},
            {"id": 9, "name": "Problema 9", "description": "descrição 9","active":True,"updated_at":"2021-08-26T00:00:00","category_id": 1},
            {"id": 10, "name": "Problema 10", "description": "descrição 10", "active":True,"updated_at":"2020-07-22T00:00:00","category_id": 1},
        ]
    }
def test_get_problemid(client):
    response = client.get("/problema/?id=1")
    assert response.status_code == 200

def test_get_problemcategoryid(client):
    response = client.get("/problema/?category_id=1")
    assert response.status_code == 200