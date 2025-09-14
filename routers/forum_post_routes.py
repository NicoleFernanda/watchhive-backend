from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from controllers.forum_post_controller import create_forum_post, delete_forum_post, read_forum_post, update_forum_post
from database import get_session
from exceptions.permission_error import PermissionError
from exceptions.record_not_found_error import RecordNotFoundError
from models.user_model import User
from schemas.commons_schemas import FilterPage, Message
from schemas.forum_schemas import CreateForumPostSchema, GetForumPostSchema
from security import get_current_user

forum_post_router = APIRouter(prefix="/forum_posts", tags=['forum_posts'])
Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@forum_post_router.post('/', status_code=HTTPStatus.CREATED, response_model=GetForumPostSchema)
async def create(post: CreateForumPostSchema, current_user: CurrentUser, session: Session):

    return await create_forum_post(
        title=post.title,
        content=post.content,
        user_id=current_user.id,
        session=session
    )


@forum_post_router.put('/{forum_post_id}', status_code=HTTPStatus.OK, response_model=GetForumPostSchema)
async def update(
    forum_post_id: int,
    forum_post: CreateForumPostSchema,
    session: Session,
    current_user: CurrentUser
):
    try:
        return await update_forum_post(
            forum_post_id=forum_post_id,
            title=forum_post.title,
            content=forum_post.content,
            logger_user_id=current_user.id,
            session=session,
        )
    except PermissionError as p:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail=str(p))
    except RecordNotFoundError as u:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(u))


@forum_post_router.delete('/{post_id}', response_model=Message)
async def delete(
    post_id: int,
    session: Session,
    current_user: CurrentUser
):
    try:
        await delete_forum_post(
            current_user_id=current_user.id,
            post_id=post_id,
            session=session,
        )
        return {'message': 'Post apagado.'}
    except PermissionError as p:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail=str(p))
    except RecordNotFoundError as u:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(u))


@forum_post_router.get('/{post_id}', response_model=GetForumPostSchema)
async def read(
    post_id: int,
    session: Session,
    current_user: CurrentUser
):
    try:
        return await read_forum_post(
            post_id=post_id,
            session=session,
        )
    except PermissionError as p:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail=str(p))
    except RecordNotFoundError as u:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(u))

