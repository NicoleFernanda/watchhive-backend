from http import HTTPStatus


def test_create_forum_comment(client, user, token, forum_post):
    response = client.post(
        f'/forum_posts/{forum_post.id}',
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


def test_create_forum_comment_post_not_found(client, token,):
    response = client.post(
        '/forum_posts/1',
        json={
            'content': 'indico bela e a fera.'
        },
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Post não encontrado no fórum WatchHive.'}


def test_delete_forum_comment_from_comment_creator(client, other_user, token, forum_post):
    forum_post.user_id = other_user.id
    response = client.post(
        f'/forum_posts/{forum_post.id}',
        json={
            'content': 'indico bela e a fera.'
        },
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.CREATED

    response = client.delete(
        f'/forum_posts/{forum_post.id}/1',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Comentário apagado.'}


def test_delete_forum_comment_from_post_creator(client, user, token, forum_comment, forum_post, other_user):
    forum_post.user_id = user.id
    forum_comment.user_id = other_user.id
    forum_comment.post_id = forum_post.id

    response = client.delete(
        f'/forum_posts/{forum_post.id}/{forum_comment.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Comentário apagado.'}


def test_delete_forum_comment_forbidden(client, other_user, token, forum_post, forum_comment):
    forum_post.user_id = 777
    forum_comment.user_id = other_user.id
    forum_comment.post_id = forum_post.id

    response = client.delete(
        f'/forum_posts/{forum_post.id}/{forum_comment.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Você não pode apagar esse comentário.'}


def test_delete_forum_comment_not_found(client, token, forum_post):
    response = client.delete(
        f'/forum_posts/{forum_post.id}/1',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Comentário não encontrado.'}