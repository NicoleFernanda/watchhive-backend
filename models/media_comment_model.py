from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class MediaComment(Base):
    __tablename__ = "media_comment"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    media_id: Mapped[int] = mapped_column(ForeignKey('media.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    content: Mapped[str]

    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
