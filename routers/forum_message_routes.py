from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from controllers.forum_comment_controller import create_forum_message, delete_forum_message
from database import get_session
from exceptions.permission_error import PermissionError
from exceptions.record_not_found_error import RecordNotFoundError
from models.user_model import User
from schemas.commons_schemas import Message
from schemas.forum_schemas import CreateForumMessageSchema, GetForumMessageSchema
from security import get_current_user

forum_message_router = APIRouter(prefix='/forum_groups', tags=['forum_messages'])
Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@forum_message_router.post('/{id_forum_group}', status_code=HTTPStatus.CREATED, response_model=GetForumMessageSchema)
async def create(id_forum_group: int, comment: CreateForumMessageSchema, current_user: CurrentUser, session: Session):

    try:
        return await create_forum_message(
            id_forum_post=id_forum_group,
            content=comment.content,
            user_id=current_user.id,
            session=session
        )
    except RecordNotFoundError as u:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(u))
    except PermissionError as p:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail=str(p))


@forum_message_router.delete('/{id_forum_group}/{id_message}', response_model=Message)
async def delete(id_forum_group: int, id_message: int, current_user: CurrentUser, session: Session):
    try:
        await delete_forum_message(
            current_user_id=current_user.id,
            post_id=id_forum_group,
            comment_id=id_message,
            session=session,
        )
        return {'message': 'Mensagem apagada.'}
    except PermissionError as p:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail=str(p))
    except RecordNotFoundError as u:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(u))
