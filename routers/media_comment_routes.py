from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from controllers.media_comment_controller import create_media_comment, delete_media_comment
from database import get_session
from exceptions.permission_error import PermissionError
from exceptions.record_not_found_error import RecordNotFoundError
from models.user_model import User
from schemas.commons_schemas import Message
from schemas.media_schemas import CreateMediaCommentSchema, GetMediaCommentSchema
from security import get_current_user

media_comment_router = APIRouter(prefix='/medias', tags=['media', 'media_comment'])
Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@media_comment_router.post('/{id_media}/comment', status_code=HTTPStatus.CREATED, response_model=GetMediaCommentSchema)
async def create(id_media: int, comment: CreateMediaCommentSchema, current_user: CurrentUser, session: Session):

    try:
        return await create_media_comment(
            media_id=id_media,
            content=comment.content,
            user_id=current_user.id,
            session=session
        )
    except RecordNotFoundError as u:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(u))


@media_comment_router.delete('/{id_media}/comment/{id_comment}', response_model=Message)
async def delete(id_media: int, id_comment: int, current_user: CurrentUser, session: Session):
    try:
        await delete_media_comment(
            media_id=id_media,
            current_user_id=current_user.id,
            comment_id=id_comment,
            session=session,
        )
        return {'message': 'Comentário apagado.'}
    except PermissionError as p:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail=str(p))
    except RecordNotFoundError as u:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(u))


