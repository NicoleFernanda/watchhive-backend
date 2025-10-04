from pydantic import BaseModel, EmailStr

from schemas.user_schemas import TokentUserSchema


class Token(BaseModel):
    access_token: str  # bearer token
    token_type: str
    user: TokentUserSchema
