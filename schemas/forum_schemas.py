from pydantic import BaseModel


# comments
class CreateForumCommentSchema(BaseModel):
    content: str


class GetForumCommentSchema(BaseModel):
    id: int
    user_id: int
    content: str


# posts
class CreateForumPostSchema(BaseModel):
    title: str
    content: str


class GetForumPostSchema(CreateForumPostSchema):
    id: int
    user_id: int
    comments: list[GetForumCommentSchema]

    class Config:
        from_attributes = True


class GetForumPostListSchema(BaseModel):
    posts: list[GetForumPostSchema]
