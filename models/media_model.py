from datetime import date
from typing import List

from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.media_comment_model import MediaComment

from .base import Base

# tabela de associação
media_genre = Table(
    "media_genre",
    Base.metadata,
    Column("media_id", ForeignKey("media.id", ondelete="CASCADE"), primary_key=True),
    Column("genre_id", ForeignKey("genre.id", ondelete="CASCADE"), primary_key=True),
)


class Genre(Base):
    __tablename__ = "genre"

    id: Mapped[int] = mapped_column(init=True, primary_key=True)
    name: Mapped[str]

    medias: Mapped[List["Media"]] = relationship(
        secondary=media_genre, back_populates="genres"
    )


class Media(Base):
    __tablename__ = "media"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    id_themoviedb: Mapped[int]
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

    genres: Mapped[List["Genre"]] = relationship(
        secondary=media_genre, back_populates="medias", init=False
    )

    comments: Mapped[list['MediaComment']] = relationship(
        init=False,
        cascade='all, delete-orphan',
        lazy='selectin',
    )
