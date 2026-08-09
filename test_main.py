from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_hello():
    response = client.get("/hello")

    assert response.status_code == 200
    assert response.json() == {"message": "hello from Docker v2"}


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_ready():
    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ready"}