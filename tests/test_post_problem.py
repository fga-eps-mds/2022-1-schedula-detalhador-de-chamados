def test_post_problem(client):
    response = client.post(
        "/problema/",
        json={"name": "test", "description": "test", "category_id": 1},
    )
    assert response.status_code == 201


def test_put_problem(client):
    response = client.put(
        "/problema/1",
        json={"name": "test", "description": "test", "category_id": 1},
    )
    assert response.status_code == 200


def test_delete_problem(client):
    response = client.delete("/problema/1")
    assert response.status_code == 200
