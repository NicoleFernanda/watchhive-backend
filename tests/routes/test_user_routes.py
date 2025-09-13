from http import HTTPStatus

from schemas.user_schemas import GetUserSchema


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }


def test_create_user_same_username(client, user):
    response = client.post(
        '/users/',
        json={
            'username': user.username,
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Opa! Username em uso.'}


def test_create_user_same_email(client, user):
    response = client.post(
        '/users/',
        json={
            'username': "alice",
            'email': user.email,
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Opa! Email em uso.'}


def test_read_users(client, user, token):
    user_response = GetUserSchema.model_validate(user).model_dump()

    response = client.get('/users', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [user_response]
    }


def test_update_user(client, user, token):
    response = client.put(
        '/users/1',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': user.id,
    }


def test_delete_user_forbidden(client, token, other_user):
    response = client.delete(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Usuário não possui permissão para editar informações de outro usuário.'}


def test_update_user_forbidden(client, token, other_user):
    response = client.put(
        f'/users/{other_user.id}',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Usuário não possui permissão para editar informações de outro usuário.'}


def test_get_user_should_return_not_found(client, other_user):
    response = client.get('/users/777')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Usuário não encontrado.'}


def test_get_user(client, user):
    response = client.get(f'/users/{user.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': user.username,
        'email': user.email,
        'id': user.id,
    }


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Usuário apagado.'}


def test_update_integrity_error(client, user, token):
    # Inserindo fausto
    client.post(
        '/users',
        json={
            'username': 'fausto',
            'email': 'fausto@example.com',
            'password': 'secret',
        },
    )

    # Alterando o user das fixture para fausto
    response_update = client.put(
        f'/users/{user.id}',
        json={
            'username': 'fausto',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {
        'detail': 'Opa! Username ou Email já existe.'
    }
