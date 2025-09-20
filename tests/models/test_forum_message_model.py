from dataclasses import asdict

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.forum_comment_model import ForumMessage
from models.forum_group_model import ForumGroup


@pytest.mark.asyncio
async def test_create_messages(session: AsyncSession, user, mock_db_time, other_user):
    with mock_db_time(model=ForumGroup) as time:
        add_post = ForumGroup(
            title='filme legal',
            content='caso alguém procura um filme lega, eu recomendo kung fu panda',
            user_id=user.id
        )

        session.add(add_post)
        await session.commit()

    with mock_db_time(model=ForumMessage) as time:
        add_comment = ForumMessage(
            content='legal, obrigada!',
            user_id=other_user.id,
            forum_group_id=add_post.id
        )

        session.add(add_comment)
        await session.commit()
        await session.refresh(add_post)

        add_post = await session.scalar(select(ForumGroup).where(ForumGroup.title == add_post.title))

    assert asdict(add_post) == {
        'id': add_post.id,
        'title': add_post.title,
        'content': add_post.content,
        'user_id': user.id,
        'created_at': time,
        'updated_at': time,
        'messages': [
            {
                'id': 1,
                'forum_group_id': add_post.id,
                'user_id': other_user.id,
                'content': add_comment.content,
                'created_at': time,
            }
        ],
    }
