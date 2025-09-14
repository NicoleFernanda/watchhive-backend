from dataclasses import asdict

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.forum_comment_model import ForumComment
from models.forum_post_model import ForumPost


@pytest.mark.asyncio
async def test_create_comment(session: AsyncSession, user, mock_db_time, other_user):
    with mock_db_time(model=ForumPost) as time:
        add_post = ForumPost(
            title='filme legal',
            content='caso alguém procura um filme lega, eu recomendo kung fu panda',
            user_id=user.id
        )

        session.add(add_post)
        await session.commit()

    with mock_db_time(model=ForumComment) as time:
        add_comment = ForumComment(
            content='legal, obrigada!',
            user_id=other_user.id,
            forum_post_id=add_post.id
        )

        session.add(add_comment)
        await session.commit()
        await session.refresh(add_post)

        add_post = await session.scalar(select(ForumPost).where(ForumPost.title == add_post.title))

    assert asdict(add_post) == {
        'id': add_post.id,
        'title': add_post.title,
        'content': add_post.content,
        'user_id': user.id,
        'created_at': time,
        'updated_at': time,
        'comments': [
            {
                'id': 1,
                'forum_post_id': add_post.id,
                'user_id': other_user.id,
                'content': add_comment.content,
                'created_at': time,
            }
        ],
    }
