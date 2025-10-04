
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from models.user_model import User
from schemas.auth_schemas import Token
from security import create_access_token, get_current_user, verify_password

auth_router = APIRouter(prefix="/auth", tags=['auth'])
OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@auth_router.post('/token', response_model=Token)  # tipo um login
async def login_for_access_token(
    form_data: OAuth2Form,
    session: Session
):
    user = await session.scalar(select(User).where(User.email == form_data.username))

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='E-mail não cadastrado.'
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Senha incorreta.'
        )

    access_token = create_access_token(
        data={'sub': user.email}
    )

    return {'access_token': access_token, 'token_type': 'Bearer', 'user': user}


@auth_router.post('/refresh_token', response_model=Token)
async def refresh_access_token(user: CurrentUser):
    new_access_token = create_access_token(data={'sub': user.email})

    return {'access_token': new_access_token, 'token_type': 'Bearer'}
