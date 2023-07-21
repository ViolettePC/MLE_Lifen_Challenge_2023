from fastapi.testclient import TestClient
from lifen_app.asgi import app

client = TestClient(app)


def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.text == '"pong"'


def test_post_patient_name_detected(document_test_dict, expected_response):
    response = client.post("patient_name_detection", json=document_test_dict)

    assert response.status_code == 200
    assert response.json() == expected_response
