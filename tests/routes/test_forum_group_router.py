from http import HTTPStatus


def test_create_forum_group(client, user, token):
    response = client.post(
        '/forum_groups/',
        json={
            'title': 'filme para assistir sexta-feira a noite',
            'content': 'indicação de filme para eu assistir com o namorado.'
        },
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'title': 'filme para assistir sexta-feira a noite',
        'content': 'indicação de filme para eu assistir com o namorado.',
        'id': 1,
        'user_id': user.id,
        'messages': []
    }


def test_update_forum_group(client, user, token, forum_group):
    forum_group.user_id = user.id
    response = client.put(
        f'/forum_groups/{forum_group.id}',
        json={
            'title': 'new title',
            'content': 'hihihi',
        },
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'title': 'new title',
        'content': 'hihihi',
        'user_id': user.id,
        'id': forum_group.id,
        'messages': [],
    }


def test_update_forum_group_forbidden(client, other_user, token, forum_group):
    forum_group.user_id = other_user.id
    response = client.put(
        f'/forum_groups/{forum_group.id}',
        json={
            'title': 'new title',
            'content': 'hihihi',
        },
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Usuário não possui permissão para editar informações de outro usuário.'}


def test_update_forum_group_not_found(client, token):
    response = client.put(
        '/forum_groups/1',
        json={
            'title': 'new title',
            'content': 'hihihi',
        },
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Grupo não encontrado no fórum WatchHive.'}


def test_delete_forum_group(client, user, token, forum_group):
    forum_group.user_id = user.id
    response = client.delete(
        f'/forum_groups/{forum_group.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Grupo apagado.'}


def test_delete_forum_group_forbidden(client, other_user, token, forum_group):
    forum_group.user_id = other_user.id
    response = client.delete(
        f'/forum_groups/{forum_group.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Usuário não possui permissão para editar informações de outro usuário.'}


def test_delete_forum_group_not_found(client, token):
    response = client.delete(
        '/forum_groups/1',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Grupo não encontrado no fórum WatchHive.'}


def test_read_post(client, token, forum_group, user):
    forum_group.user_id = user.id

    response = client.get(
        f'/forum_groups/{forum_group.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': forum_group.id,
        'title': forum_group.title,
        'content': forum_group.content,
        'user_id': user.id,
        'messages': [],
    }


def test_read_forum_group_not_found(client, token):
    response = client.get(
        '/forum_groups/1',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Grupo não encontrado no fórum WatchHive.'}
