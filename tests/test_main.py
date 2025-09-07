

def test_return_hello_world(client):
    response = client.get('/')

    assert response.json() == {"Hello": "World"}
