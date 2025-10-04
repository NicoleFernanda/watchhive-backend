from pydantic import BaseModel, ConfigDict, EmailStr


class CreateUserSchema(BaseModel):
    name: str
    email: EmailStr  # formato de e-mail, com o @
    password: str
    profile_picture: str | None


class GetUserSchema(BaseModel):
    id: int
    username: str
    name: str
    email: EmailStr
    profile_picture: str | None

    model_config = ConfigDict(from_attributes=True)


class GetUserListSchema(BaseModel):
    users: list[GetUserSchema]


class TokentUserSchema(BaseModel):
    id: int
    name: str
    email: EmailStr
    profile_picture: str | None

    model_config = ConfigDict(from_attributes=True)
