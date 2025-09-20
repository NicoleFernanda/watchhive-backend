from dataclasses import asdict

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.forum_group_model import ForumGroup


@pytest.mark.asyncio
async def test_create_group(session: AsyncSession, user, mock_db_time):
    with mock_db_time(model=ForumGroup) as time:
        new_post = ForumGroup(
            title='filme legal',
            content='caso alguém procura um filme lega, eu recomendo kung fu panda',
            user_id=user.id
        )

        session.add(new_post)
        await session.commit()

        post = await session.scalar(select(ForumGroup).where(ForumGroup.title == new_post.title))

    assert asdict(post) == {
        'id': 1,
        'title': new_post.title,
        'content': new_post.content,
        'user_id': user.id,
        'created_at': time,
        'updated_at': time,
        'messages': [],
    }
