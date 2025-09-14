from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class ForumComment(Base):
    __tablename__ = 'forum_comment'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    content: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    forum_post_id: Mapped[int] = mapped_column(ForeignKey('forum_post.id'))

    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
