from http import HTTPStatus


def test_create_forum_post(client, user, token):
    response = client.post(
        '/forum_posts/',
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
        'user_id': user.id
    }


def test_update_forum_post(client, user, token, forum_post):
    forum_post.user_id = user.id
    response = client.put(
        f'/forum_posts/{forum_post.id}',
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
        'id': forum_post.id
    }


def test_update_forum_post_forbidden(client, other_user, token, forum_post):
    forum_post.user_id = other_user.id
    response = client.put(
        f'/forum_posts/{forum_post.id}',
        json={
            'title': 'new title',
            'content': 'hihihi',
        },
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Usuário não possui permissão para editar informações de outro usuário.'}


def test_delete_forum_post(client, user, token, forum_post):
    forum_post.user_id = user.id
    response = client.delete(
        f'/forum_posts/{forum_post.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Post apagado.'}


def test_delete_forum_post_forbidden(client, other_user, token, forum_post):
    forum_post.user_id = other_user.id
    response = client.delete(
        f'/forum_posts/{forum_post.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Usuário não possui permissão para editar informações de outro usuário.'}