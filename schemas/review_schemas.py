from pydantic import BaseModel


class CreateReviewSchema(BaseModel):
    score: int


class GetReviewSchema(BaseModel):
    id: int
    media_id: int
    user_id: int
    score: int


class GetPublicReviewFollowerSchema(BaseModel):
    user_id: int
    score: int
    media_title: str
    media_id: int
    media_poster_url: str


class GetPublicReviewsFollowerSchema(BaseModel):
    reviews: list[GetPublicReviewFollowerSchema]