from http import HTTPStatus


def test_create_comment_in_media_not_found(client, token):
    response = client.post(
        f'/medias/1/comment',
        json={
            'content': 'pior parte do filme foi que acabou.'
        },
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Título não encontrado no WatchHive.'}


def test_create_comment(client, user, token, media):
    response = client.post(
        f'/medias/{media.id}/comment',
        json={
            'content': 'pior parte do filme foi que acabou.'
        },
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "id": 1,
        "content": "pior parte do filme foi que acabou.",
        "user_id": user.id
    }


def test_delete_comment(client, user, token, media, media_comment):
    media_comment.media_id = media.id
    media_comment.user_id = user.id

    response = client.delete(
        f'/medias/{media.id}/comment/{media_comment.id}',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Comentário apagado.'}


def test_delete_comment_permission_error(client, token, media, media_comment, other_user):
    media_comment.media_id = media.id
    media_comment.user_id = other_user.id

    response = client.delete(
        f'/medias/{media.id}/comment/{media_comment.id}',
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Usuário não possui permissão para editar informações de outro usuário.'}


def test_delete_comment_not_found(client, token, media):
    response = client.delete(
        f'/medias/{media.id}/comment/1',
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Comentário não encontrado.'}


def test_delete_comment_media_not_found(client, token, media_comment):
    response = client.delete(
        f'/medias/2/comment/{media_comment.id}',
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Título não encontrado no WatchHive.'}
