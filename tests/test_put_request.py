def test_put_request(client):
    response = client.put(
        "/chamado/1",
        json={
            "applicant_name": "Fulano de Tal",
            "applicant_phone": "999999999",
            "place": "Sala de Testes",
            "description": "Ta tudo dando errado nos testes.",
            "workstation_id": 2,
            "problems": [
                {
                    "problem_id": 1,
                    "is_event": False,
                    "request_status": "pending",
                    "priority": "hight",
                },
                {
                    "problem_id": 2,
                    "is_event": False,
                    "request_status": "pending",
                    "priority": "urgent",
                },
            ],
        },
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Dados atualizados com sucesso"
    assert response.json()["data"][0]["applicant_name"] == "Fulano de Tal"


def test_put_request_attendant_name(client):
    response = client.put(
        "/chamado/1",
        json={
            "attendant_name": "Fulano",
            "applicant_name": "Fulano de Tal",
            "applicant_phone": "999999999",
            "place": "Sala de Testes",
            "description": "Ta tudo dando errado nos testes.",
            "workstation_id": 2,
            "problems": [
                {
                    "problem_id": 1,
                    "is_event": False,
                    "request_status": "pending",
                    "priority": "hight",
                },
                {
                    "problem_id": 2,
                    "is_event": False,
                    "request_status": "pending",
                    "priority": "urgent",
                },
            ],
        },
    )
    assert response.status_code == 400
