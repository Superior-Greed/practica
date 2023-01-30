from fastapi.testclient import TestClient


def test_read_main(app):
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}