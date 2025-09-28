from pydantic import BaseModel


class CreateReviewSchema(BaseModel):
    score: int


class GetReviewSchema(BaseModel):
    id: int
    media_id: int
    user_id: int
    score: int