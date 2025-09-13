from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from controllers.user_controller import validate_user
from exceptions.permission_error import PermissionError
from exceptions.record_not_found_error import RecordNotFoundError
from models.forum_post_model import ForumPost


async def create_forum_post(title: str, content: str, user_id: id, session: AsyncSession) -> ForumPost:
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
        new_post (ForumPost): post adicionado no banco de dados.
    """
    new_post = ForumPost(
        content=content,
        title=title,
        user_id=user_id
    )

    session.add(new_post)
    await session.commit()
    await session.refresh(new_post)

    return new_post


async def update_forum_post(
        forum_post_id: id,
        title: str,
        content: str,
        logger_user_id: id,
        session: AsyncSession
    ) -> ForumPost:
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
        new_post (ForumPost): post adicionado no banco de dados.
    """

    # checa se o post existe
    post = await existing_forum_post(forum_post_id, session)

    # checa se o id do usuario do post é o mesmo que está logado
    validate_user(logger_user_id, post.user_id)

    # update
    post.title = title
    post.content = content

    await session.commit()
    await session.refresh(post)

    return post


async def delete_forum_post(current_user_id: int, post_id: int, session: AsyncSession):
    """
    Apaga um usuário do banco de dados.

    Args:
        current_user(User): usuário logado.
        post_id (int): post a "mexido", passado pela url.
        session (AsyncSession): sessão do banco de dados ativa.

    Raises:
        PermissionError: caso o usuário a ser utilizado em operações não seja o mesmo logado.
            No caso, quando alguém está tentando alterar o perfil de outra pessoa.
    """

    post = await existing_forum_post(post_id, session)

    validate_user(logger_user_id=current_user_id, user_id_passed=post.user_id)

    await session.delete(post)
    await session.commit()


async def existing_forum_post(id_forum_post: int, session: AsyncSession) -> ForumPost:
    """
    Método responsável por validar se o post existe e, caso seja verdade, o retorne.

    Args:
        logger_user_id (int): id do usuário logado.
        user_id_passed (int): id passado na url.

    Raises:
        PermissionError: caso o usuário a ser utilizado em operações não seja o mesmo logado.
            No caso, quando alguém está tentando alterar o perfil de outra pessoa.
    """
    existing_post = await session.scalar(select(ForumPost).where((ForumPost.id == id_forum_post)))

    if not existing_post:
        raise RecordNotFoundError('Post não encontrado no fórum WatchHive.')

    return existing_post


