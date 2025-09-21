
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class ForumParticipant(Base):
    __tablename__ = 'forum_participant'

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), primary_key=True)
    forum_group_id: Mapped[int] = mapped_column(ForeignKey('forum_group.id'), primary_key=True)
