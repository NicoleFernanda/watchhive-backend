from datetime import date

from pydantic import BaseModel, ConfigDict, Field

from schemas.commons_schemas import FilterPage


# genre
class GetGenre(BaseModel):
    id: int

    model_config = ConfigDict(from_attributes=True)


# comments
class CreateMediaCommentSchema(BaseModel):
    content: str


class GetMediaCommentSchema(BaseModel):
    id: int
    user_id: int
    content: str

    model_config = ConfigDict(from_attributes=True)


class GetPublicCommentSchema(BaseModel):
    content: str
    media_title: str
    media_id: int
    media_poster_url: str


# media
class GetMediaSchema(BaseModel):
    id: int
    title: str
    original_title: str | None
    description: str | None
    dt_launch: date | None
    original_language: str | None
    media_type: str
    poster_url: str | None
    adult: bool | None

    genres: list[GetGenre]

    comments: list[GetMediaCommentSchema]

    average_score: float

    vote_count: int

    user_review: int | None = None

    model_config = ConfigDict(from_attributes=True)


class SendTopMediasInfoSchema(BaseModel):
    genre_id: int
    movie: bool


class FilterMedia(BaseModel):
    genre_id: int = Field(description="ID do gênero a ser buscado")
    movie: bool = Field(description="True para filme, False para série")


class FilterMediaSearch(FilterPage):
    term: str = Field()


class FilterMediaShow(BaseModel):
    offset: int = Field(0, ge=0)
    limit: int = Field(50, ge=1)
    genre_id: int = Field(description="ID do gênero a ser buscado")
    movie: bool = Field(description="True para filme, False para série")


class ShowMediaInListSchema(BaseModel):
    id: int
    title: str
    poster_url: str | None


class ShowMediasInListSchema(BaseModel):
    medias: list[ShowMediaInListSchema]
