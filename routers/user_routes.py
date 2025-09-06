from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from database import get_session
from models.user_model import User
from schemas.user_schemas import CreateUserSchema, GetUserListSchema, GetUserSchema, Message
from security import get_password_hash

user_router = APIRouter(prefix="/users")

database = []


@user_router.post('/', status_code=HTTPStatus.CREATED, response_model=GetUserSchema)
def create(user: CreateUserSchema, session: Session = Depends(get_session)):

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
def read_all(limit: int = 10, offset: int = 0, session: Session = Depends(get_session)):
    users = session.scalars(select(User).limit(limit).offset(offset))
    return {"users": users}


@user_router.put('/{user_id}', status_code=HTTPStatus.OK, response_model=GetUserSchema)
def update(user_id: int, user: CreateUserSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where((User.id == user_id)))

    if not db_user:
        raise HTTPException(detail='Usuário não encontrado.', status_code=HTTPStatus.NOT_FOUND)

    try:
        db_user.username = user.username
        db_user.password = get_password_hash(user.password)
        db_user.email = user.email
        session.commit()
        session.refresh(db_user)

        return db_user

    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or Email already exists',
        )


@user_router.delete('/{user_id}', response_model=Message)
def delete(user_id: int,  session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado.'
        )

    session.delete(db_user)
    session.commit()

    return {'message': 'Usuário apagado.'}


@user_router.get('/{user_id}', response_model=GetUserSchema)
def read_user(user_id: int,  session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where((User.id == user_id)))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado.'
        )

    return db_user
