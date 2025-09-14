from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from controllers.forum_comment_controller import create_forum_comment, delete_forum_comment
from database import get_session
from exceptions.permission_error import PermissionError
from exceptions.record_not_found_error import RecordNotFoundError
from models.user_model import User
from schemas.commons_schemas import Message
from schemas.forum_schemas import CreateForumCommentSchema, GetForumCommentSchema
from security import get_current_user

forum_comment_router = APIRouter(prefix='/forum_posts', tags=['forum_comments'])
Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@forum_comment_router.post('/{id_post}', status_code=HTTPStatus.CREATED, response_model=GetForumCommentSchema)
async def create(id_post: int, comment: CreateForumCommentSchema, current_user: CurrentUser, session: Session):

    try:
        return await create_forum_comment(
            id_post=id_post,
            content=comment.content,
            user_id=current_user.id,
            session=session
        )
    except RecordNotFoundError as u:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(u))


@forum_comment_router.delete('/{id_post}/{id_comment}', response_model=Message)
async def delete(id_post: int, id_comment: int, current_user: CurrentUser, session: Session):
    try:
        await delete_forum_comment(
            current_user_id=current_user.id,
            post_id=id_post,
            comment_id=id_comment,
            session=session,
        )
        return {'message': 'Comentário apagado.'}
    except PermissionError as p:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail=str(p))
    except RecordNotFoundError as u:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(u))
