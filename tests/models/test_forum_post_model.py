from dataclasses import asdict

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.forum_post_model import ForumPost


@pytest.mark.asyncio
async def test_create_post(session: AsyncSession, user, mock_db_time):
    with mock_db_time(model=ForumPost) as time:
        new_post = ForumPost(
            title='filme legal',
            content='caso alguém procura um filme lega, eu recomendo kung fu panda',
            user_id=user.id
        )

        session.add(new_post)
        await session.commit()

        post = await session.scalar(select(ForumPost).where(ForumPost.title == new_post.title))

    assert asdict(post) == {
        'id': 1,
        'title': new_post.title,
        'content': new_post.content,
        'user_id': user.id,
        'created_at': time,
        'updated_at': time,
        'comments': [],
    }
