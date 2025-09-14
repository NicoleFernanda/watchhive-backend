from datetime import date

from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Media(Base):
    __tablename__ = "media"

    id: Mapped[int] = mapped_column(init=True, primary_key=True)
    id_imdb: Mapped[str]

    title: Mapped[str] = mapped_column(index=True)
    original_title: Mapped[str] = mapped_column(index=True, nullable=True)
    description: Mapped[str] = mapped_column(nullable=True)

    dt_launch: Mapped[date] = mapped_column(nullable=True)
    original_language: Mapped[str] = mapped_column(nullable=True)
    media_type: Mapped[str]
    poster_url: Mapped[str] = mapped_column(nullable=True)

    popularity: Mapped[float] = mapped_column(nullable=True)
    vote_average: Mapped[float] = mapped_column(nullable=True)
    vote_count: Mapped[int] = mapped_column(nullable=True)
    adult: Mapped[bool] = mapped_column(default=False)
