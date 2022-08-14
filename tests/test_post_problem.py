def test_post_problem(client):
    response = client.post(
        "/problema/",
        json={"name": "test", "description": "test", "category_id": 1},
    )
    assert response.status_code == 201
