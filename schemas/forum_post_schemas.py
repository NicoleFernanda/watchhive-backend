from pydantic import BaseModel


class CreateForumPostSchema(BaseModel):
    title: str
    content: str


class GetForumPostSchema(CreateForumPostSchema):
    id: int
    user_id: int

    class Config:
        from_attributes = True


class GetForumPostListSchema(BaseModel):
    posts: list[GetForumPostSchema]
