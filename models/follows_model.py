from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, validates

from exceptions.business_error import BusinessError

from .base import Base


class Follows(Base):
    __tablename__ = 'follows'

    follower_id: Mapped[int] = mapped_column(
        ForeignKey('user.id', ondelete='CASCADE'), 
        primary_key=True
    )

    followed_id: Mapped[int] = mapped_column(
        ForeignKey('user.id', ondelete='CASCADE'), 
        primary_key=True
    )

    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
