from pydantic import BaseModel


class Token(BaseModel):
    access_token: str  # bearer token
    token_type: str
