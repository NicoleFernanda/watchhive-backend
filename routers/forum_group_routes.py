from http import HTTPStatus
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from controllers.forum_group_controller import (
    create_forum_group,
    create_forum_group_full,
    delete_forum_group,
    read_forum_group,
    update_forum_group,
)
from controllers.forum_participant_controller import get_created_forums, get_participating_forums
from database import get_session
from exceptions.permission_error import PermissionError
from exceptions.record_not_found_error import RecordNotFoundError
from models.user_model import User
from schemas.commons_schemas import Message
from schemas.forum_schemas import (
    CreateForumGroupFullSchema,
    CreateForumGroupSchema,
    GetForumGroupFullSchema,
    GetForumGroupListSchema,
)
from security import get_current_user

forum_group_router = APIRouter(prefix="/forum_groups", tags=['forum_groups'])
Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@forum_group_router.post('/', status_code=HTTPStatus.CREATED, response_model=GetForumGroupFullSchema)
async def create(group: CreateForumGroupSchema, current_user: CurrentUser, session: Session):

    return await create_forum_group(
        title=group.title,
        content=group.content,
        user_id=current_user.id,
        session=session
    )


@forum_group_router.post('/full', status_code=HTTPStatus.CREATED, response_model=GetForumGroupFullSchema)
async def create_full(group: CreateForumGroupFullSchema, current_user: CurrentUser, session: Session):

    participant_ids: List[int] = [p.user_id for p in group.participants]

    return await create_forum_group_full(
        title=group.title,
        content=group.content,
        participants=participant_ids,
        user_id=current_user.id,
        session=session
    )


@forum_group_router.get('/created', response_model=GetForumGroupListSchema)
async def read_creator_groups(
    session: Session,
    current_user: CurrentUser
):
    try:
        forums = await get_created_forums(
            user_id=current_user.id,
            session=session,
        )

        return {'groups': forums}
    except RecordNotFoundError as u:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(u))


@forum_group_router.get('/participating', response_model=GetForumGroupListSchema)
async def read_participating_groups(
    session: Session,
    current_user: CurrentUser
):
    try:
        forums = await get_participating_forums(
            user_id=current_user.id,
            session=session,
        )

        return {'groups': forums}
    except RecordNotFoundError as u:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(u))


@forum_group_router.put('/{forum_group_id}', status_code=HTTPStatus.OK, response_model=GetForumGroupFullSchema)
async def update(
    forum_group_id: int,
    forum_group: CreateForumGroupSchema,
    session: Session,
    current_user: CurrentUser
):
    try:
        return await update_forum_group(
            forum_post_id=forum_group_id,
            title=forum_group.title,
            content=forum_group.content,
            logger_user_id=current_user.id,
            session=session,
        )
    except PermissionError as p:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail=str(p))
    except RecordNotFoundError as u:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(u))


@forum_group_router.delete('/{forum_group_id}', response_model=Message)
async def delete(
    forum_group_id: int,
    session: Session,
    current_user: CurrentUser
):
    try:
        await delete_forum_group(
            current_user_id=current_user.id,
            post_id=forum_group_id,
            session=session,
        )
        return {'message': 'Grupo apagado.'}
    except PermissionError as p:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail=str(p))
    except RecordNotFoundError as u:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(u))


@forum_group_router.get('/{forum_group_id}', response_model=GetForumGroupFullSchema)
async def read(
    forum_group_id: int,
    session: Session,
    current_user: CurrentUser
):
    try:
        return await read_forum_group(
            post_id=forum_group_id,
            session=session,
        )
    except RecordNotFoundError as u:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(u))
