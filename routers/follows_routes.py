from http import HTTPStatus
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from controllers.follows_controller import (
    follow_user,
    get_following_users_comments,
    get_following_users_reviews,
    unfollow_user,
)
from database import get_session
from exceptions.business_error import BusinessError
from exceptions.record_not_found_error import RecordNotFoundError
from models.user_model import User
from schemas.commons_schemas import Message
from schemas.media_schemas import GetPublicCommentFollowerSchema, GetPublicCommentsFollowerSchema
from schemas.review_schemas import GetPublicReviewFollowerSchema, GetPublicReviewsFollowerSchema
from security import get_current_user

follows_router = APIRouter(prefix="/users", tags=['users'])
Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@follows_router.get('/following/comments', response_model=GetPublicCommentsFollowerSchema)
async def get_following_latest_comments(
    current_user: CurrentUser,
    session: Session,
):
    try:
        comments = await get_following_users_comments(
            current_user_id=current_user.id,
            session=session,
        )

        return {'comments': comments}
    except RecordNotFoundError as u:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(u))


@follows_router.get('/following/reviews', response_model=GetPublicReviewsFollowerSchema)
async def get_following_latest_reviews(
    current_user: CurrentUser,
    session: Session,
):
    try:
        reviews = await get_following_users_reviews(
            current_user_id=current_user.id,
            session=session,
        )
    
        return {'reviews': reviews}
    except RecordNotFoundError as u:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(u))


@follows_router.post('/{user_id}/follow', status_code=HTTPStatus.OK, response_model=Message)
async def create(user_id: int, current_user: CurrentUser, session: Session):

    try:
        await follow_user(
            current_user_id=current_user.id,
            user_to_follow_id=user_id,
            session=session,
        )
        return {'message': 'Passou a seguir usuário.'}
    except BusinessError as u:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=str(u))
    except RecordNotFoundError as r:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(r))


@follows_router.delete('/{user_id}/unfollow', status_code=HTTPStatus.OK, response_model=Message)
async def delete(
    user_id: int,
    session: Session,
    current_user: CurrentUser
):
    await unfollow_user(
        current_user_id=current_user.id,
        user_to_unfollow_id=user_id,
        session=session,
    )
    return {'message': 'Deixou de seguir usuário.'}
