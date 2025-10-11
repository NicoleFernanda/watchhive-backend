from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from controllers.user_controller import validate_user
from exceptions.record_not_found_error import RecordNotFoundError
from models.forum_group_model import ForumGroup
from models.forum_participant_model import ForumParticipant


async def create_forum_group(title: str, content: str, user_id: id, session: AsyncSession) -> ForumGroup:
    """
    Método para criação de um grupo no fórum watchhive, pegando o usuário logado.
    Assim que o grupo for criado, o criador dele é adicionado automaticamente aos participantes.

    Args:
        title (str): username do usuário.
        content (str): conteúdo do post.
        user_id (str): id do usuário logado.
        session (AsyncSession): sessão do banco de dados ativa.
        
    Raises:
        BusinessError: caso o email ou username já estiverem em uso.
    
    Returns:
        new_forum_group (ForumGroup): grupo adicionado no banco de dados.
    """
    new_forum_group = ForumGroup(
        content=content,
        title=title,
        user_id=user_id
    )

    session.add(new_forum_group)
    await session.commit()
    await session.refresh(new_forum_group)

    new_participant = ForumParticipant(
        user_id=user_id,
        forum_group_id=new_forum_group.id
    )

    session.add(new_participant)
    await session.commit()
    await session.refresh(new_participant)

    return new_forum_group


async def create_forum_group_full(
    title: str,
    content: str,
    participants: List[int], # Lista de schemas de participantes
    user_id: int, # O ID do criador do grupo (será o primeiro participante)
    session: AsyncSession
) -> 'ForumGroup':
    """
    Cria um novo ForumGroup e adiciona o criador e outros usuários como participantes.
    """
    
    new_group = ForumGroup(
        title=title,
        content=content,
        user_id=user_id # user_id é o criador
    )

    session.add(new_group)
    await session.flush()
    
    # Garante que o criador do grupo também seja um participante
    all_participant_ids = set(participants)
    all_participant_ids.add(user_id)
    
    participant_objects = []
    for p_id in all_participant_ids:
        participant = ForumParticipant(
            user_id=p_id,
            forum_group_id=new_group.id
        )
        participant_objects.append(participant)

    session.add_all(participant_objects)
    
    await session.commit()
    await session.refresh(new_group) 
    return new_group


async def update_forum_group(
        forum_post_id: id,
        title: str,
        content: str,
        logger_user_id: id,
        session: AsyncSession
    ) -> ForumGroup:
    """
    Método para criação de um post no fórum watchhive, pegando o usuário logado.

    Args:
        title (str): username do usuário.
        content (str): conteúdo do post.
        user_id (str): id do usuário logado.
        session (AsyncSession): sessão do banco de dados ativa.
        
    Raises:
        BusinessError: caso o email ou username já estiverem em uso.
    
    Returns:
        post (ForumGroup): grupo atualizado no banco de dados.
    """

    # checa se o post existe
    post = await existing_forum_group(forum_post_id, session)

    # checa se o id do usuario do post é o mesmo que está logado
    validate_user(logger_user_id, post.user_id)

    # update
    post.title = title
    post.content = content

    await session.commit()
    await session.refresh(post)

    return post


async def delete_forum_group(current_user_id: int, post_id: int, session: AsyncSession):
    """
    Apaga um grupo do banco de dados.

    Args:
        current_user(User): usuário logado.
        post_id (int): post a "mexido", passado pela url.
        session (AsyncSession): sessão do banco de dados ativa.

    Raises:
        PermissionError: caso o usuário a ser utilizado em operações não seja o mesmo logado.
            No caso, quando alguém está tentando alterar o perfil de outra pessoa.
    """

    post = await existing_forum_group(post_id, session)

    validate_user(logger_user_id=current_user_id, user_id_passed=post.user_id)

    await session.delete(post)
    await session.commit()


async def read_forum_group(post_id: int, session: AsyncSession):
    """
    Método retorna um post específico.

    Args:
        post_id (int): id do post em questão.
        session (AsyncSession): sessão ativa do banco de dados.
    """
    return await existing_forum_group(post_id, session)


async def existing_forum_group(id_forum_group: int, session: AsyncSession) -> ForumGroup:
    """
    Método responsável por validar se o grupo existe e, caso seja verdade, o retorne.

    Args:
        logger_user_id (int): id do usuário logado.
        user_id_passed (int): id passado na url.

    Raises:
        RecordNotFoundError: caso o usuário a ser utilizado em operações não seja o mesmo logado.
            No caso, quando alguém está tentando alterar o perfil de outra pessoa.
    """
    existing_post = await session.scalar(select(ForumGroup).where((ForumGroup.id == id_forum_group)))

    if not existing_post:
        raise RecordNotFoundError('Grupo não encontrado no fórum WatchHive.')

    return existing_post
