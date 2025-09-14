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
        'user_id': user.id,
        'comments': []
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
        'id': forum_post.id,
        'comments': [],
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


def test_update_forum_post_not_found(client, token):
    response = client.put(
        f'/forum_posts/1',
        json={
            'title': 'new title',
            'content': 'hihihi',
        },
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Post não encontrado no fórum WatchHive.'}


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


def test_delete_forum_post_not_found(client, token):
    response = client.delete(
        f'/forum_posts/1',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Post não encontrado no fórum WatchHive.'}


def test_read_post(client, token, forum_post, user):
    forum_post.user_id = user.id

    response = client.get(
        f'/forum_posts/{forum_post.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': forum_post.id,
        'title': forum_post.title,
        'content': forum_post.content,
        'user_id': user.id,
        'comments': [],
    }


def test_read_forum_post_not_found(client, token):
    response = client.get(
        f'/forum_posts/1',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Post não encontrado no fórum WatchHive.'}
