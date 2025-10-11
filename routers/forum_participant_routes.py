from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from controllers.forum_participant_controller import create_forum_participant, delete_forum_participant
from database import get_session
from exceptions.business_error import BusinessError
from exceptions.permission_error import PermissionError
from exceptions.record_not_found_error import RecordNotFoundError
from models.user_model import User
from schemas.commons_schemas import Message
from schemas.forum_schemas import CreateForumParticipantSchema, GetForumParticipantSchema
from security import get_current_user

forum_participant_router = APIRouter(prefix='/forum_groups', tags=['forum_participants'])
Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@forum_participant_router.post('/{id_forum_group}/participants', status_code=HTTPStatus.CREATED, response_model=GetForumParticipantSchema)
async def create(id_forum_group: int, participant: CreateForumParticipantSchema, current_user: CurrentUser, session: Session):

    try:
        return await create_forum_participant(
            id_forum_group=id_forum_group,
            participant_id=participant.user_id,
            current_user_id=current_user.id,
            session=session
        )
    except RecordNotFoundError as u:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(u))
    except PermissionError as p:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail=str(p))
    except BusinessError as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))


@forum_participant_router.delete('/{id_forum_group}/participants/{id_participant}', status_code=HTTPStatus.CREATED, response_model=Message)
async def delete(id_forum_group: int, id_participant: int, current_user: CurrentUser, session: Session):

    try:
        await delete_forum_participant(
            id_forum_group=id_forum_group,
            participant_id=id_participant,
            current_user_id=current_user.id,
            session=session
        )

        return {'message': 'Usuário removido.'}
    except RecordNotFoundError as u:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(u))
    except PermissionError as p:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail=str(p))
    except BusinessError as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))
