from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from controllers.review_controller import create_review, update_review
from database import get_session
from exceptions.business_error import BusinessError
from exceptions.record_not_found_error import RecordNotFoundError
from models.user_model import User
from schemas.review_schemas import CreateReviewSchema, GetReviewSchema
from security import get_current_user

review_router = APIRouter(prefix='/medias', tags=['forum_messages'])
Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@review_router.post('/{id_media}/review', status_code=HTTPStatus.CREATED, response_model=GetReviewSchema)
async def create(id_media: int, review: CreateReviewSchema, current_user: CurrentUser, session: Session):

    try:
        return await create_review(
            media_id=id_media,
            score=review.score,
            user_id=current_user.id,
            session=session
        )
    except RecordNotFoundError as u:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(u))
    except BusinessError as e:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=str(e))


@review_router.put('/{id_media}/review', status_code=HTTPStatus.OK, response_model=GetReviewSchema)
async def create(id_media: int, review: CreateReviewSchema, current_user: CurrentUser, session: Session):

    try:
        return await update_review(
            media_id=id_media,
            score=review.score,
            user_id=current_user.id,
            session=session
        )
    except RecordNotFoundError as u:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(u))
    except BusinessError as e:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=str(e))
