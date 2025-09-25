from http import HTTPStatus


def test_read_media_not_found(client, token):
    response = client.get(
        f'/medias/1',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Título não encontrado no WatchHive.'}


def test_read_media(client, user, token, media):
    response = client.get(f'/medias/{media.id}', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": media.id,
        "title": media.title,
        "original_title": media.original_title,
        "description": media.description,
        "dt_launch": str(media.dt_launch),
        "original_language": media.original_language,
        "media_type": media.media_type,
        "poster_url": media.poster_url,
        "adult": media.adult,
        "genres": [],
        "comments": []
    }
