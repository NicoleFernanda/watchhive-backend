from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from controllers.forum_post_controller import existing_forum_post
from controllers.user_controller import validate_user
from exceptions.permission_error import PermissionError
from exceptions.record_not_found_error import RecordNotFoundError
from models.forum_comment_model import ForumComment
from models.forum_post_model import ForumPost


async def create_forum_comment(id_post: str, content: str, user_id: id, session: AsyncSession) -> ForumComment:
    """
    Método para criação de um comentário de um post no fórum watchhive, pegando o usuário logado.

    Args:
        id_post (int): id do post a ser comentado.
        content (str): conteúdo do post.
        user_id (str): id do usuário logado.
        session (AsyncSession): sessão do banco de dados ativa.
        
    Raises:
        BusinessError: caso o email ou username já estiverem em uso.
    
    Returns:
        comment (ForumComment): comentário adicionado ao post.
    """
    post = await existing_forum_post(id_post, session)
    
    comment = ForumComment(
        content=content,
        user_id=user_id,
        forum_post_id=post.id
    )

    session.add(comment)
    await session.commit()
    await session.refresh(comment)

    return comment


async def delete_forum_comment(post_id: int, comment_id, current_user_id: int, session: AsyncSession):
    """
    Método responsável para apagar um comentário feito dentro de um post.
    Quem pode apagar é o próprio criador do comentário OU o dono do post que foi comentaedo.
    """

    post = await existing_forum_post(post_id, session)
    comment = await existing_forum_comment(comment_id, session)

    if post.user_id == current_user_id or comment.user_id == current_user_id:
        await session.delete(comment)
        await session.commit()
        await session.refresh(post)
        return
    
    raise PermissionError('Você não pode apagar esse comentário.')

async def existing_forum_comment(id_comment: int, session: AsyncSession):
    """
    Verifica a existência do comentário em questão. Caso exista, seu objeto 
    será retornado. Caso conterário, uma exceção será lançada.

    Args:
        id_comment (int): id do comentário.
        session (AsyncSession): sessão ativa do banco de dados.

    Raises:
        RecordNotFound: caso o comentário não exista.
    """

    existing_comment = await session.scalar(select(ForumComment).where((ForumComment.id == id_comment)))

    if not existing_comment:
        raise RecordNotFoundError('Comentário não encontrado.')

    return existing_comment