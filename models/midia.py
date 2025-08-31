from enum import Enum
from sqlalchemy import Boolean, Column, Date, Double, Float, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import relationship

from db.database import Base


class TypeMidiaEnum(str, Enum):
    FILME = "movie"
    SÉRIE = "tv"


midia_genre = Table(
    "midia_genre",
    Base.metadata,
    Column("midia_id", Integer, ForeignKey("midia.id"), primary_key=True),
    Column("genre_id", Integer, ForeignKey("genre.id"), primary_key=True),
)


class Midia(Base):
    __tablename__ = "midia"

    id = Column(Integer, primary_key=True, index=True)          # id
    id_imdb = Column(String, unique=True, index=True)           # id_imdb

    ds_title = Column(String, index=True)                       # titulo
    ds_original_name = Column(String)                           # titulo_original
    ds_description = Column(Text, nullable=True)                # descricao

    dt_launch = Column(Date)                                    # data_lancamento
    ds_original_language = Column(String)                       # lingua_original
    ds_midia_type = Column(String)                              # tipo_midia
    ds_poster_url = Column(String, nullable=True)               # poster_url

    di_popularity = Column(Float, nullable=True)                # popularity
    di_vote_average = Column(Float, nullable=True)              # vote_average
    di_vote_count = Column(Integer, nullable=True)              # vote_count
    fl_adult = Column(Boolean, default=False)                   # adult

    genres = relationship(
        "Genre",
        secondary=midia_genre,
        back_populates="midias"
    )


class Genre(Base):
    __tablename__ = "genre"

    id = Column(Integer, primary_key=True)            # ID do TMDB
    ds_description = Column(String, unique=True)     # Nome do gênero

    midias = relationship(
        "Midia",
        secondary=midia_genre,
        back_populates="genres"
    )
