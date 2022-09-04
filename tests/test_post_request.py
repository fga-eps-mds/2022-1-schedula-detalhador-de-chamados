def test_post_request(client):
    response = client.post(
        "/chamado",
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
                },
                {
                    "category_id": 1,
                    "problem_id": 2,
                    "is_event": True,
                    "description": "Chamado sobre acesso a internet.",
                    "request_status": "pending",
                    "priority": "normal",
                },
            ],
        },
    )
    assert response.status_code == 201


def test_post_request_invalid(client):
    response = client.post(
        "/chamado",
        json={
            "attendant_name": "Fulano",
            "applicant_name": "Ciclano",
            "applicant_phone": "1111111111",
            "place": "Sala de Reuniões",
            "description": "Chamado aberto para acesso a internet.",
            "problems": [
                {
                    "problem_id": 1,
                    "is_event": False,
                    "request_status": "pending",
                    "priority": "normal",
                },
                {
                    "problem_id": 2,
                    "is_event": False,
                    "request_status": "pending",
                    "priority": "normal",
                },
            ],
        },
    )
    assert response.status_code == 422
