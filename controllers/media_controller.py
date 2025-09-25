from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from controllers.user_controller import validate_user
from exceptions.record_not_found_error import RecordNotFoundError
from models.media_model import Media


async def get_media(media_id: int, session: AsyncSession):
    """
    Método retorna um post específico.

    Args:
        media_id (int): id do filme ou série.
        session (AsyncSession): sessão ativa do banco de dados.
    """
    return await existing_media(media_id, session)


async def existing_media(media_id: int, session: AsyncSession) -> Media:
    """
    Método responsável por validar se o filme ou série existe e, caso seja verdade, o retorne.

    Args:
        media_id (int): id do filme ou série.
        session (AsyncSession): sessão ativa do banco.

    Raises:
        RecordNotFoundError: caso a mídia pesquisada não seja encontrada.
    """
    media = await session.scalar(
        select(Media)
        .options(selectinload(Media.genres))
        .options(selectinload(Media.comments))
        .where((Media.id == media_id))
    )

    if not media:
        raise RecordNotFoundError('Título não encontrado no WatchHive.')

    return media