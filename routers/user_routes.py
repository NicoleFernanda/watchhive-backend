from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from controllers.user_controller import create_user, delete_user, get_all_users, get_user, update_user
from database import get_session
from exceptions.business_error import BusinessError
from exceptions.permission_error import PermissionError
from exceptions.record_not_found_error import RecordNotFoundError
from models.user_model import User
from schemas.commons_schemas import FilterPage, Message
from schemas.user_schemas import CreateUserSchema, GetUserListSchema, GetUserSchema
from security import get_current_user

user_router = APIRouter(prefix="/users", tags=['users'])
Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@user_router.post('/', status_code=HTTPStatus.CREATED, response_model=GetUserSchema)
async def create(user: CreateUserSchema, session: Session):

    try:
        return await create_user(
            name=user.name,
            profile_picture=user.profile_picture,
            email=user.email,
            password=user.password,
            session=session,
        )
    except BusinessError as u:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=str(u))


@user_router.get('/', status_code=HTTPStatus.OK, response_model=GetUserListSchema)
async def read_all(
    session: Session,
    current_user: CurrentUser,
    filter_users: Annotated[FilterPage, Query()]
):

    users = await get_all_users(
        limit=filter_users.limit,
        offset=filter_users.offset,
        session=session
    )
    return {"users": users}


@user_router.put('/{user_id}', status_code=HTTPStatus.OK, response_model=GetUserSchema)
async def update(
    user_id: int,
    user: CreateUserSchema,
    session: Session,
    current_user: CurrentUser
):

    try:
        return await update_user(
            current_user=current_user,
            user_id=user_id,
            username=user.username,
            email=user.email,
            password=user.password,
            session=session,
        )
    except PermissionError as p:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail=str(p))
    except BusinessError as u:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=str(u))


@user_router.delete('/{user_id}', response_model=Message)
async def delete(
    user_id: int,
    session: Session,
    current_user: CurrentUser
):
    try:
        await delete_user(
            current_user=current_user,
            user_id=user_id,
            session=session,
        )
        return {'message': 'Usuário apagado.'}
    except PermissionError as p:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail=str(p))


@user_router.get('/{user_id}', response_model=GetUserSchema)
async def read_user(
    user_id: int,
    session: Session,
):
    # TODO AAA: adicionar permissão para pesquisar usuários também kk
    try:
        return await get_user(
            user_id=user_id,
            session=session,
        )
    except RecordNotFoundError as u:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(u))
