from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.forum_message_model import ForumMessage
from models.forum_participant_model import ForumParticipant

from .base import Base


class ForumGroup(Base):
    __tablename__ = 'forum_group'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    title: Mapped[str]
    content: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))

    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now(), server_onupdate=func.now(),
    )

    messages: Mapped[list['ForumMessage']] = relationship(
        init=False,
        cascade='all, delete-orphan',
        lazy='selectin',
    )

    participants: Mapped[list['ForumParticipant']] = relationship(
        init=False,
        cascade='all, delete-orphan',
        lazy='selectin',
    )
