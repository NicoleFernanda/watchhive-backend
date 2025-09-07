
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_session
from models.user_model import User
from security import create_access_token, verify_password

auth_router = APIRouter(prefix="/auth", tags=['auth'])
OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
T_Session = Annotated[Session, Depends(get_session)]


@auth_router.post('/token')  # tipo um login
def login_for_access_token(
    form_data: OAuth2Form,
    session: T_Session
):
    user = session.scalar(select(User).where(User.email == form_data.username))

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

    return {'access_token': access_token, 'token_type': 'Bearer'}
