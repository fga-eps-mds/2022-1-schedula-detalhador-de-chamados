# def test_get_request(client):
#     url = "/chamado"
#     response = client.get(url)
#     assert response.status_code == 200
#     assert response.json()["message"] == "Dados buscados com sucesso"


# def test_get_requestid(client):
#     url = "/chamado?problem_id=1"
#     response = client.get(url)
#     assert response.status_code == 200


# def test_get_requestid_invalid(client):
#     url = "/chamado?problem_id=99"
#     response = client.get(url)
#     assert response.status_code == 200
#     assert (
#         response.json()["message"]
#         == "Nenhum chamado com esse tipo de problema encontrado"
#     )
