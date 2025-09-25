from dataclasses import asdict
from datetime import date, datetime

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.media_model import Media, MediaComment


@pytest.mark.asyncio
async def test_create_media_comment(session: AsyncSession, mock_db_time, user):
    with mock_db_time(model=Media) as time:
        media = Media(
            id_themoviedb=2,
            id_imdb=2,
            title="kung fu panda 2",
            original_title="kung fu panda 2",
            description="po vai atrás do ganso",
            dt_launch=time.date(),
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

    created_media = await session.scalar(select(Media).options(selectinload(Media.genres)).where(Media.id == 1))

    with mock_db_time(model=MediaComment) as time:
        comment = MediaComment(
            media_id=created_media.id,
            user_id=user.id,
            content="AMO ESSE FILME"
        )

        session.add(comment)
        await session.commit()
        session.refresh(media)

        assert asdict(media) == {
            'id': 1,
            'adult': False,
            'description': 'po vai atrás do ganso',
            'dt_launch': time.date(),
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
            "genres": [],
            "comments": []
        }
