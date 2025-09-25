from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from controllers.media_controller import existing_media
from controllers.user_controller import validate_user
from exceptions.record_not_found_error import RecordNotFoundError
from models.media_model import Media, MediaComment


async def create_media_comment(media_id: int, content: str, user_id: int, session: AsyncSession) -> MediaComment:
    """
    Cria um comentário para filme ou série.

    Args:
        media_id (int): id so filme ou série.
        content (str): conteúdo do comentário, em si.
        user_id (int): usuário quem criou o comentário.
        session (AsyncSession): sessão ativa do banco de dados.
    """

    media = await existing_media(media_id, session)

    new_comment = MediaComment(
        media_id = media_id,
        user_id=user_id,
        content=content
    )

    session.add(new_comment)
    await session.commit()
    await session.refresh(new_comment)
    await session.refresh(media)

    return new_comment


async def delete_media_comment(media_id: int, comment_id: int, current_user_id: int, session: AsyncSession) -> None:
    """
   Deleta um comentário para filme ou série.

    Args:
        comment_id (int): id do comentário.
        current_user_id (int): id do usuário logado.
        session (AsyncSession): sessão ativa do banco de dados.
    """

    await existing_media(media_id, session)

    comment = await session.scalar(
        select(MediaComment)
        .where((MediaComment.id == comment_id))
    )

    if not comment:
        raise RecordNotFoundError("Comentário não encontrado.")
    
    validate_user(current_user_id, comment.user_id)

    await session.delete(comment)
    await session.commit()
