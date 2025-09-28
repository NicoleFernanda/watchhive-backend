from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, validates

from exceptions.business_error import BusinessError

from .base import Base


class Review(Base):
    __tablename__ = 'review'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    score: Mapped[int]
    media_id: Mapped[int] = mapped_column(ForeignKey('media.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))

    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )

    @validates('score')
    def validate_score(self, key, score):
        if score <= 0 or score > 5:
            raise BusinessError("A avaliação deve ser entre 1 e 5")
        return score
