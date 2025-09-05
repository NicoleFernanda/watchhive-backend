from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


class CreateUserSchema(BaseModel):
    username: str
    email: EmailStr  # formato de e-mail, com o @
    password: str


class GetUserSchema(BaseModel):
    id: int
    username: str
    email: EmailStr


class CreateUserDatabaseSchema(GetUserSchema):
    id: int


class GetUserListSchema(BaseModel):
    users: list[GetUserSchema]
