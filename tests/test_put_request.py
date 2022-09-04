def test_put_request(client):
    response = client.put(
        "/chamado/4",
        json={
            "attendant_name": "Fulano",
            "applicant_name": "Ciclano",
            "applicant_phone": "1111111111",
            "city_id": 1,
            "workstation_id": 1,
            "problems": [
                {
                    "category_id": 1,
                    "problem_id": 1,
                    "is_event": False,
                    "request_status": "pending",
                    "description": "Chamado sobre acesso a internet.",
                    "priority": "normal",
                    "alert_dates": [],
                },
                {
                    "category_id": 1,
                    "problem_id": 2,
                    "is_event": True,
                    "description": "Chamado sobre acesso a internet.",
                    "request_status": "pending",
                    "priority": "normal",
                    "alert_dates": [],
                },
            ],
        },
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Dados atualizados com sucesso"
    assert response.json()["data"][0]["applicant_name"] == "Ciclano"


def test_put_request_attendant_name(client):
    response = client.put(
        "/chamado/4",
        json={
            "attendant_name": "Ciclaninho",
            "applicant_name": "Fulaninho de Tal",
            "applicant_phone": "1111111111",
            "city_id": 1,
            "workstation_id": 1,
            "problems": [
                {
                    "category_id": 1,
                    "problem_id": 1,
                    "is_event": False,
                    "request_status": "pending",
                    "description": "Chamado sobre acesso a internet.",
                    "priority": "normal",
                },
                {
                    "category_id": 1,
                    "problem_id": 2,
                    "is_event": True,
                    "description": "Chamado sobre acesso a internet.",
                    "request_status": "pending",
                    "priority": "normal",
                    "alert_dates": [],
                },
            ],
        },
    )
    assert response.status_code == 200
