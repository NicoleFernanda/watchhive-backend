from pydantic import BaseModel, ConfigDict, EmailStr


class CreateUserSchema(BaseModel):
    name: str
    email: EmailStr  # formato de e-mail, com o @
    password: str
    avatar: int = 1


class PatchUserSchema(BaseModel):
    name: str | None = None
    avatar: int | None = None
    password: str | None = None


class GetUserSchema(BaseModel):
    id: int
    username: str
    name: str
    email: EmailStr
    avatar: int

    model_config = ConfigDict(from_attributes=True)


class GetUserListSchema(BaseModel):
    users: list[GetUserSchema]


class TokentUserSchema(BaseModel):
    id: int
    name: str
    email: EmailStr
    avatar: int

    model_config = ConfigDict(from_attributes=True)
