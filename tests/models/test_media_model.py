from dataclasses import asdict
from datetime import date

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.media_model import Media


@pytest.mark.asyncio
async def test_create_media(session: AsyncSession, mock_db_time):
    media = Media(
        id_themoviedb=2,
        id_imdb=2,
        title="kung fu panda 2",
        original_title="kung fu panda 2",
        description="po vai atrás do ganso",
        dt_launch=date(2025, 9, 14),
        original_language='en',
        media_type='filme',
        poster_url="",
        popularity=1,
        vote_average=2,
        vote_count=3,
        adult=False
    )

    session.add(media)
    await session.commit()

    user = await session.scalar(select(Media).options(selectinload(Media.genres)).where(Media.id == 1))

    assert asdict(user) == {
        'id': 1,
        'adult': False,
        'description': 'po vai atrás do ganso',
        'dt_launch': date(2025, 9, 14),
        'id_imdb': 2,
        'id_themoviedb': 2,
        'media_type': 'filme',
        'original_language': 'en',
        'original_title': 'kung fu panda 2',
        'popularity': 1,
        'poster_url': '',
        'title': 'kung fu panda 2',
        'vote_average': 2,
        'vote_count': 3,
        "genres": []
    }
