from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from controllers.user_list_controller import add_to_list_to_watch
from database import get_session
from exceptions.business_error import BusinessError
from exceptions.permission_error import PermissionError
from exceptions.record_not_found_error import RecordNotFoundError
from models.user_model import User
from schemas.commons_schemas import FilterPage, Message
from schemas.user_schemas import CreateUserSchema, GetUserListSchema, GetUserSchema
from security import get_current_user

user_list_router = APIRouter(prefix="/medias", tags=['medias'])
Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@user_list_router.post('/{media_id}/lists/to-watch', status_code=HTTPStatus.CREATED, response_model=Message)
async def create(media_id: int, current_user: CurrentUser, session: Session):

    try:
        await add_to_list_to_watch(
            user_id=current_user.id,
            media_id=media_id,
            session=session,
        )

        return {'message': 'Título adicionado a lista com sucesso!'}
    except BusinessError as u:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=str(u))
    except RecordNotFoundError as r:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(r))
