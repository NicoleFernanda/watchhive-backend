from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from controllers.user_controller import (
    create_user,
    delete_user,
    get_all_users,
    get_public_user_profile,
    get_user,
    patch_user,
    search_users_by_term,
    update_user,
)
from database import get_session
from exceptions.business_error import BusinessError
from exceptions.permission_error import PermissionError
from exceptions.record_not_found_error import RecordNotFoundError
from models.user_model import User
from schemas.commons_schemas import FilterPage, Message
from schemas.user_schemas import (
    CreateUserSchema,
    GetPublicUserSchema,
    GetUserListSchema,
    GetUserSchema,
    PatchUserSchema,
)
from security import get_current_user

user_router = APIRouter(prefix="/users", tags=['users'])
Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@user_router.post('/', status_code=HTTPStatus.CREATED, response_model=GetUserSchema)
async def create(user: CreateUserSchema, session: Session):

    try:
        return await create_user(
            name=user.name,
            avatar=user.avatar,
            email=user.email,
            password=user.password,
            session=session,
        )
    except BusinessError as u:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=str(u))


@user_router.get('/me', response_model=GetUserSchema)
async def read_user_me(
    current_user: CurrentUser,
    session: Session,
):
    try:
        return await get_user(
            user_id=current_user.id,
            session=session,
        )
    except RecordNotFoundError as u:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(u))


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


@user_router.get('/search', response_model=GetUserListSchema)
async def search_user(
    current_user: CurrentUser,
    session: Session,
    term: str = Query(None, description="Termo de pesquisa para nome ou username do usuário."),
):

    users = await search_users_by_term(
        search_term=term,
        session=session,
    )

    return {'users': users}


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


@user_router.patch('/', status_code=HTTPStatus.OK, response_model=GetUserSchema)
async def patch(
    user: PatchUserSchema,
    session: Session,
    current_user: CurrentUser
):

    return await patch_user(
        current_user=current_user,
        name=user.name,
        password=current_user.password,
        avatar=user.avatar,
        session=session,
    )


@user_router.get("/{target_user_id}", response_model=GetPublicUserSchema)
async def read_user(
    target_user_id: int,
    current_user: CurrentUser,
    session: Session,
):
    try:
        profile = await get_public_user_profile(
            session,
            target_user_id=target_user_id,
            current_user_id=current_user.id
        )

        return profile
    except RecordNotFoundError as p:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(p))
    except Exception as e:
        # AQUI VOCÊ CAPTURA QUALQUER NOVO ERRO (QUE ESTÁ DANDO O SEU 500)
        # print(f"Erro inesperado no perfil: {e}") # Loga no servidor

        # O detail VAI EXPÔR O ERRO NO FRONT-END, PERMITINDO O DIAGNÓSTICO
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"ERRO DE SERVIDOR INESPERADO: {type(e).__name__} - {str(e)}"
        )
