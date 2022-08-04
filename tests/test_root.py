def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"APP": "Detalhador de chamados is running"}
    
