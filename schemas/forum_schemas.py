from pydantic import BaseModel


# comments
class CreateForumMessageSchema(BaseModel):
    content: str


class GetForumMessageSchema(BaseModel):
    id: int
    user_id: int
    content: str


# posts
class CreateForumGroupSchema(BaseModel):
    title: str
    content: str


class GetForumGroupSchema(CreateForumGroupSchema):
    id: int
    user_id: int
    messages: list[GetForumMessageSchema]

    class Config:
        from_attributes = True


class GetForumGroupListSchema(BaseModel):
    groups: list[GetForumGroupSchema]
