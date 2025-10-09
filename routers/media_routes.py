# criar get
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import Field
from sqlalchemy.ext.asyncio import AsyncSession

from controllers.media_controller import get_media, get_random_medias, search_medias_by_title
from database import get_session
from exceptions.permission_error import PermissionError
from exceptions.record_not_found_error import RecordNotFoundError
from models.user_model import User
from schemas.commons_schemas import FilterPage, Message
from schemas.media_schemas import FilterMedia, FilterMediaSearch, GetMediaSchema, ShowMediasInListSchema, SendTopMediasInfoSchema
from security import get_current_user

media_router = APIRouter(prefix='/medias', tags=['media', 'media_comment'])
Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@media_router.get('/random', response_model=ShowMediasInListSchema)
async def read_top_medias(
    current_user: CurrentUser,
    session: Session,
    filter_media: Annotated[FilterMedia, Query()]
):
    
    medias = await get_random_medias(
        genre_id=filter_media.genre_id,
        movie=filter_media.movie,
        session=session,
    )

    return {'medias': medias}


@media_router.get('/search', response_model=ShowMediasInListSchema)
async def read_top_medias(
    current_user: CurrentUser,
    session: Session,
    filter_page: Annotated[FilterMediaSearch, Query()],
):
    
    medias = await search_medias_by_title(
        search_term=filter_page.term,
        session=session,
        offset=filter_page.offset,
        limit=filter_page.limit,
    )

    return {'medias': medias}


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
