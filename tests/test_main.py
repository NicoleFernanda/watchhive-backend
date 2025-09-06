from http import HTTPStatus


def test_return_hello_world(client):
    response = client.get('/')

    assert response.json() == {"Hello": "World"}


def test_get_token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password}
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token
