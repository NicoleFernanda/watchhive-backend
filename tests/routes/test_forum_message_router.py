from http import HTTPStatus


def test_create_forum_message_participant(client, user, token, forum_group, forum_participant):
    response = client.post(
        f'/forum_groups/{forum_group.id}',
        json={
            'content': 'indico bela e a fera.'
        },
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'content': 'indico bela e a fera.',
        'id': 1,
        'user_id': user.id
    }


def test_create_forum_message_not_participant(client, token, forum_group, other_user):
    forum_group.user_id = other_user.id
    response = client.post(
        f'/forum_groups/{forum_group.id}',
        json={
            'content': 'indico bela e a fera.'
        },
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Você não faz parte do grupo.'}


def test_create_forum_message_post_not_found(client, token,):
    response = client.post(
        '/forum_groups/1',
        json={
            'content': 'indico bela e a fera.'
        },
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Grupo não encontrado no fórum WatchHive.'}


def test_delete_forum_message_from_message_creator(client, user, token, forum_group, forum_participant):
    response = client.post(
        f'/forum_groups/{forum_group.id}',
        json={
            'content': 'indico bela e a fera.'
        },
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.CREATED

    response = client.delete(
        f'/forum_groups/{forum_group.id}/1',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Mensagem apagada.'}


def test_delete_forum_message_from_post_creator(client, user, token, forum_message, forum_group, other_user):
    forum_group.user_id = user.id
    forum_message.user_id = other_user.id
    forum_message.forum_group_id = forum_group.id

    response = client.delete(
        f'/forum_groups/{forum_group.id}/{forum_message.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Mensagem apagada.'}


def test_delete_forum_message_forbidden(client, other_user, token, forum_group, forum_message):
    forum_group.user_id = 777
    forum_message.user_id = other_user.id
    forum_message.forum_group_id = forum_group.id

    response = client.delete(
        f'/forum_groups/{forum_group.id}/{forum_message.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Você não pode apagar essa mensagem.'}


def test_delete_forum_message_not_found(client, token, forum_group):
    response = client.delete(
        f'/forum_groups/{forum_group.id}/1',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Mensagem não encontrada.'}
