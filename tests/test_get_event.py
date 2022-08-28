def test_get_event(client):
    url = "/evento"
    response = client.get(url)
    assert response.status_code == 200


def test_get_event_one_day(client):
    url = "/evento?days_to_event=1"
    response = client.get(url)
    assert response.status_code == 200
    assert response.json()["data"] == []
