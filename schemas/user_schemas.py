from pydantic import BaseModel, ConfigDict, EmailStr


class CreateUserSchema(BaseModel):
    username: str
    email: EmailStr  # formato de e-mail, com o @
    password: str


class GetUserSchema(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class GetUserListSchema(BaseModel):
    users: list[GetUserSchema]
