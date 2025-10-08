# criar get
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from controllers.media_controller import get_media, get_random_medias
from database import get_session
from exceptions.permission_error import PermissionError
from exceptions.record_not_found_error import RecordNotFoundError
from models.user_model import User
from schemas.commons_schemas import Message
from schemas.media_schemas import GetMediaSchema, GetMediasSchema, SendTopMediasInfoSchema
from security import get_current_user

media_router = APIRouter(prefix='/medias', tags=['media', 'media_comment'])
Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]

@media_router.get('/{media_id}', response_model=GetMediaSchema)
async def read_media(
    media_id: int,
    current_user: CurrentUser,
    session: Session,
):
    try:
        return await get_media(
            media_id=media_id,
            session=session,
        )
    except RecordNotFoundError as u:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(u))
    

@media_router.get('/top/20', response_model=GetMediasSchema)
async def read_top_medias(
    current_user: CurrentUser,
    session: Session,
    query_info: SendTopMediasInfoSchema,
):
    
    medias = await get_random_medias(
        genre_id=query_info.genre_id,
        movie=query_info.movie,
        session=session,
    )

    return {'medias': medias}
