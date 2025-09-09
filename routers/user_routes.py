from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from models.user_model import User
from schemas.commons_schemas import FilterPage, Message
from schemas.user_schemas import CreateUserSchema, GetUserListSchema, GetUserSchema
from security import get_current_user, get_password_hash

user_router = APIRouter(prefix="/users", tags=['users'])
Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@user_router.post('/', status_code=HTTPStatus.CREATED, response_model=GetUserSchema)
async def create(user: CreateUserSchema, session: Session):

    db_user = await session.scalar(
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
    await session.commit()
    await session.refresh(db_user)

    return db_user


@user_router.get('/', status_code=HTTPStatus.OK, response_model=GetUserListSchema)
async def read_all(
    session: Session,
    current_user: CurrentUser,
    filter_users: Annotated[FilterPage, Query()]
):
    users = await session.scalars(select(User).limit(filter_users.limit).offset(filter_users.offset))
    return {"users": users}


@user_router.put('/{user_id}', status_code=HTTPStatus.OK, response_model=GetUserSchema)
async def update(
    user_id: int,
    user: CreateUserSchema,
    session: Session,
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
        await session.commit()
        await session.refresh(current_user)

        return current_user

    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username ou Email já existe.',
        )


@user_router.delete('/{user_id}', response_model=Message)
async def delete(
    user_id: int,
    session: Session,
    current_user: CurrentUser
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Usuário não possui permissão para deletar outro usuário.'
        )

    session.delete(current_user)
    await session.commit()

    return {'message': 'Usuário apagado.'}


@user_router.get('/{user_id}', response_model=GetUserSchema)
async def read_user(user_id: int, session: Session):
    db_user = await session.scalar(select(User).where((User.id == user_id)))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado.'
        )

    return db_user
