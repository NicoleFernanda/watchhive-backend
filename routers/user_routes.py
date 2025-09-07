from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from schemas.commons_schemas import FilterPage, Message
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import get_session
from models.user_model import User
from schemas.user_schemas import CreateUserSchema, GetUserListSchema, GetUserSchema
from security import get_current_user, get_password_hash

user_router = APIRouter(prefix="/users", tags=['users'])
T_Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@user_router.post('/', status_code=HTTPStatus.CREATED, response_model=GetUserSchema)
def create(user: CreateUserSchema, session: T_Session):

    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Username already exists',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Email already exists',
            )

    db_user = User(
        username=user.username, password=get_password_hash(user.password), email=user.email
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@user_router.get('/', status_code=HTTPStatus.OK, response_model=GetUserListSchema)
def read_all(
    session: T_Session,
    current_user: CurrentUser,
    filter_users: Annotated[FilterPage, Query()]
):
    users = session.scalars(select(User).limit(filter_users.limit).offset(filter_users.offset))
    return {"users": users}


@user_router.put('/{user_id}', status_code=HTTPStatus.OK, response_model=GetUserSchema)
def update(
    user_id: int,
    user: CreateUserSchema,
    session: T_Session,
    current_user: CurrentUser
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Usuário não possui permissão para editar informações de outro usuário.'
        )

    try:
        current_user.username = user.username
        current_user.password = get_password_hash(user.password)
        current_user.email = user.email
        session.commit()
        session.refresh(current_user)

        return current_user

    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username ou Email já existe.',
        )


@user_router.delete('/{user_id}', response_model=Message)
def delete(
    user_id: int,
    session: T_Session,
    current_user: CurrentUser
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Usuário não possui permissão para deletar outro usuário.'
        )

    session.delete(current_user)
    session.commit()

    return {'message': 'Usuário apagado.'}


@user_router.get('/{user_id}', response_model=GetUserSchema)
def read_user(user_id: int, session: T_Session):
    db_user = session.scalar(select(User).where((User.id == user_id)))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado.'
        )

    return db_user
