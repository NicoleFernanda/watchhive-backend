from datetime import date
from pydantic import BaseModel, ConfigDict


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

    model_config = ConfigDict(from_attributes=True)
