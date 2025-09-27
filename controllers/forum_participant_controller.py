from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from controllers.forum_group_controller import existing_forum_group
from controllers.media_controller import existing_media
from controllers.user_controller import existing_user, validate_user
from exceptions.business_error import BusinessError
from exceptions.record_not_found_error import RecordNotFoundError
from models.forum_group_model import ForumGroup
from models.forum_participant_model import ForumParticipant
from models.media_model import Media, MediaComment


async def create_forum_participant(participant_id: int, id_forum_group: int, current_user_id: int, session: AsyncSession) -> MediaComment:
    """
    Adiciona um participante a um grupo.

    Args:
        participant_id (int): id do usuário a ser adicionado ao fórum.
        id_forum_group (int): id do grupo do fórum a ser "editado".
        current_user_id (int): usuário quem fez a requisição.
        session (AsyncSession): sessão ativa do banco de dados.
    """

    forum_group = await existing_forum_group(id_forum_group, session)

    participant = await existing_forum_participant(id_forum_group, participant_id, session)
    
    # preciso validar se quem está tentando adicionar o usuario é o criador
    validate_user(current_user_id, forum_group.user_id)

    # verifico se já está no grupo
    if participant:
        raise BusinessError('Usuário já inserido no grupo.')

    # valido se usuário existe
    await existing_user(participant_id, session)    

    new_participant = ForumParticipant(
        user_id=participant_id,
        forum_group_id=id_forum_group
    )

    # session add commit refresh
    session.add(new_participant)
    await session.commit()

    await session.refresh(new_participant)
    await session.refresh(forum_group)

    return new_participant


async def delete_forum_participant(participant_id: int, id_forum_group: int, current_user_id: int, session: AsyncSession) -> MediaComment:
    """
    Remove um participante do grupo.

    Args:
        participant_id (int): id do usuário a ser removido ao fórum.
        id_forum_group (int): id do grupo do fórum a ser "editado".
        current_user_id (int): usuário quem fez a requisição.
        session (AsyncSession): sessão ativa do banco de dados.
    """

    forum_group = await existing_forum_group(id_forum_group, session)

    participant = await existing_forum_participant(id_forum_group, participant_id, session)
    
    # preciso validar se quem está tentando adicionar o usuario é o criador
    validate_user(current_user_id, forum_group.user_id)

    # verifico se já está no grupo
    if not participant:
        raise BusinessError('Usuário não pertence ao grupo.')

    # valido se usuário existe
    await existing_user(participant_id, session)    

    # session add commit refresh
    await session.delete(participant)
    await session.commit()

    await session.refresh(forum_group)


async def existing_forum_participant(id_forum_group: int, id_participant: int, session: AsyncSession):
    """
    Valida se o participante está no grupo. Caso esteja, será retornado. Caso não, retorna None.

    Args:
        id_forum_group (int): Id do grupo do fórum em questão
        id_participant (int): Id do participante a ser procurado
        session (AsyncSession): sessão ativa do banco de dados
    """

    await existing_forum_group(id_forum_group, session)

    existing_participant = await session.scalar(
        select(ForumParticipant)
        .where((ForumParticipant.user_id == id_participant) and (ForumGroup.id == id_forum_group))
    )

    if not existing_participant:
        return None

    return existing_participant


