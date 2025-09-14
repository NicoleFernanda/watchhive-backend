from dataclasses import asdict

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.genre_model import Genre


@pytest.mark.asyncio
async def test_create_genre(session: AsyncSession):
    
    genre = Genre(id=1, name='Acao')

    session.add(genre)
    await session.commit()

    genre = await session.scalar(select(Genre).where(Genre.id == 1))

    assert asdict(genre) == {
        'id': 1,
        'name': 'Acao',
    }
