from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_return_hello_world():
    response = client.get('/')

    assert response.json() == {"Hello": "World"}
