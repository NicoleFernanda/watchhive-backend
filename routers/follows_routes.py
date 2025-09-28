from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from controllers.follows_controller import follow_user, unfollow_user
from database import get_session
from exceptions.business_error import BusinessError
from exceptions.permission_error import PermissionError
from exceptions.record_not_found_error import RecordNotFoundError
from models.user_model import User
from schemas.commons_schemas import FilterPage, Message
from schemas.user_schemas import CreateUserSchema, GetUserListSchema, GetUserSchema
from security import get_current_user

follows_router = APIRouter(prefix="/users", tags=['users'])
Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


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
