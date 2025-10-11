from pydantic import BaseModel


# comments
class CreateForumMessageSchema(BaseModel):
    content: str


class GetForumMessageSchema(BaseModel):
    id: int
    user_id: int
    content: str


# participants
class CreateForumParticipantSchema(BaseModel):
    user_id: int


class GetForumParticipantSchema(BaseModel):
    user_id: int


# posts
class CreateForumGroupFullSchema(BaseModel):
    title: str
    content: str
    participants: list[GetForumParticipantSchema]


class CreateForumGroupSchema(BaseModel):
    title: str
    content: str


class GetForumGroupSchema(CreateForumGroupSchema):
    id: int
    user_id: int
    messages: list[GetForumMessageSchema]
    participants: list[GetForumParticipantSchema]

    class Config:
        from_attributes = True


class GetForumGroupListSchema(BaseModel):
    groups: list[GetForumGroupSchema]
