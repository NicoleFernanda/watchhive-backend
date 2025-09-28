from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from controllers.user_controller import existing_user
from exceptions.business_error import BusinessError
from models.follows_model import Follows


async def follow_user(current_user_id: int, user_to_follow_id: int, session: AsyncSession):
    """
    Seguir um usuário específico.

    Args:
        current_user_id (int): usuário logado (quem vai seguir)
        user_to_follow_id (int): usuário a ser seguido
        session (AsyncSession): sessão do banco de dados ativa.

    Raises:
        BusinessError: caso o usuário que quer seguir seja o mesmo a ser seguido.
    """
    if user_to_follow_id == current_user_id:
        raise BusinessError("Não é possível seguir a si mesmo.")
    
    await existing_user(user_to_follow_id, session)

    follow = Follows(
        followed_id=user_to_follow_id,
        follower_id=current_user_id
    )

    session.add(follow)
    await session.commit()
    await session.refresh(follow)


async def unfollow_user(current_user_id: int, user_to_unfollow_id: int, session: AsyncSession):
    """
    Apaga um usuário do banco de dados.

    Args:
        current_user_id (int): usuário logado (quem vai seguir)
        user_to_unfollow_id (int): usuário a deixar de ser seguido
        session (AsyncSession): sessão do banco de dados ativa.

    Raises:
        PermissionError: caso o usuário a ser utilizado em operações não seja o mesmo logado.
            No caso, quando alguém está tentando alterar o perfil de outra pessoa.
    """
    follow = await session.scalar(select(Follows)
        .where(
            (Follows.followed_id == user_to_unfollow_id) 
            & 
            (Follows.follower_id == current_user_id)
        )
    )
    
    if follow:
        await session.delete(follow)
        await session.commit()
