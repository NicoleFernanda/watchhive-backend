from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from controllers.forum_group_controller import existing_forum_group
from exceptions.permission_error import PermissionError
from exceptions.record_not_found_error import RecordNotFoundError
from models.forum_comment_model import ForumMessage
from models.forum_participant_model import ForumParticipant


async def create_forum_message(id_forum_post: str, content: str, user_id: id, session: AsyncSession) -> ForumMessage:
    """
    Método para criação de um mensagem em um fórum watchhive, pegando o usuário logado.

    Args:
        id_forum_post (int): id do forúm group a ser comentado.
        content (str): conteúdo do post.
        user_id (str): id do usuário logado.
        session (AsyncSession): sessão do banco de dados ativa.
        
    Raises:
        BusinessError: caso o email ou username já estiverem em uso.
    
    Returns:
        comment (ForumComment): mensagem adicionado ao post.
    """
    group = await existing_forum_group(id_forum_post, session)

    participant = await session.scalar(select(ForumParticipant).where(ForumParticipant.user_id == user_id))

    if not participant:
        raise PermissionError('Você não faz parte do grupo.')

    comment = ForumMessage(
        content=content,
        user_id=user_id,
        forum_group_id=group.id
    )

    session.add(comment)
    await session.commit()
    await session.refresh(comment)

    return comment


async def delete_forum_message(post_id: int, comment_id, current_user_id: int, session: AsyncSession):
    """
    Método responsável para apagar um mensagem feito dentro de um fórum.
    Quem pode apagar é o próprio criador da mensagem OU o dono do fórum que foi comentaedo.
    """

    group = await existing_forum_group(post_id, session)
    comment = await existing_forum_message(comment_id, session)

    if group.user_id == current_user_id or comment.user_id == current_user_id:
        await session.delete(comment)
        await session.commit()
        await session.refresh(group)
        return

    raise PermissionError('Você não pode apagar essa mensagem.')


async def existing_forum_message(id_comment: int, session: AsyncSession):
    """
    Verifica a existência da mensagem em questão. Caso exista, seu objeto 
    será retornado. Caso conterário, uma exceção será lançada.

    Args:
        id_comment (int): id da mensagem.
        session (AsyncSession): sessão ativa do banco de dados.

    Raises:
        RecordNotFound: caso a mensagem não exista.
    """

    existing_comment = await session.scalar(select(ForumMessage).where((ForumMessage.id == id_comment)))

    if not existing_comment:
        raise RecordNotFoundError('Mensagem não encontrada.')

    return existing_comment
