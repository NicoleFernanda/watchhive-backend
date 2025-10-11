from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from controllers.user_list_controller import add_to_list_to_watch, get_all_media_from_user_list, remove_from_list_to_watch
from database import get_session
from exceptions.business_error import BusinessError
from exceptions.record_not_found_error import RecordNotFoundError
from models.user_list_model import ListType
from models.user_model import User
from schemas.commons_schemas import Message
from schemas.media_schemas import ShowMediasInListSchema
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
    

@user_list_router.delete('/{media_id}/lists/to-watch', response_model=Message)
async def delete(media_id: int, current_user: CurrentUser, session: Session):

    try:
        await remove_from_list_to_watch(
            user_id=current_user.id,
            media_id=media_id,
            session=session,
        )

        return {'message': 'Título removido a lista com sucesso!'}
    except RecordNotFoundError as r:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(r))


@user_list_router.get('/lists/to-watch', response_model=ShowMediasInListSchema)
async def get_watch(current_user: CurrentUser, session: Session):

    try:
        medias = await get_all_media_from_user_list(
            user_id=current_user.id,
            list_type=ListType.TO_WATCH,
            session=session,
        )

        return {'medias': medias}
    except RecordNotFoundError as r:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(r))
    

@user_list_router.get('/lists/watched', response_model=ShowMediasInListSchema)
async def get_watched(current_user: CurrentUser, session: Session):

    try:
        medias = await get_all_media_from_user_list(
            user_id=current_user.id,
            list_type=ListType.WATCHED,
            session=session,
        )

        return {'medias': medias}
    except RecordNotFoundError as r:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(r))