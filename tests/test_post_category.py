def test_post_category(client):
    response = client.post(
        "/categoria/", json={"name": "test", "description": "test"}
    )
    assert response.status_code == 201


def test_post_category_invalid_name(client):
    response = client.post(
        "/categoria/", json={"name": None, "description": "test"}
    )
    assert response.status_code == 422
