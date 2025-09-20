from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class ForumMessage(Base):
    __tablename__ = 'forum_message'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    content: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    forum_group_id: Mapped[int] = mapped_column(ForeignKey('forum_group.id'))

    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
