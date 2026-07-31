from http import HTTPStatus

from fastapi.testclient import TestClient

from recall_api.app import app


def test_health_check_deve_retornar_ok_e_ta_rodano():
    client = TestClient(app)

    response = client.get("/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Tá rodano!"}
