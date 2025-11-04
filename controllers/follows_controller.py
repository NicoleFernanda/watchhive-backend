from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from controllers.user_controller import existing_user
from exceptions.business_error import BusinessError
from models.follows_model import Follows
from models.media_comment_model import MediaComment
from models.media_model import Media
from models.review_model import Review


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

    already_follows = await session.scalar(
        select(Follows).where(
            Follows.follower_id == current_user_id,
            Follows.followed_id == user_to_follow_id
        )
    )

    if already_follows:
        raise BusinessError("Você já segue este usuário.")

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

    else:
        raise BusinessError("Não foi possível deixar de seguir usuário.")


async def get_following_users_comments(current_user_id: int, session: AsyncSession):
    """
    Retorna os útimos comentários de usuários dentrosdas mídias.

    Args:
        current_user_id (int): usuário logado.
        session (AsyncSession): sessão do banco de dados ativa.
    """

    stmt = (
        select(
            MediaComment.user_id.label("user_id"),
            MediaComment.content.label("content"),
            Media.title.label("media_title"),
            Media.id.label("media_id"),
            Media.poster_url.label("media_poster_url"),
        )
        .join(Follows, Follows.followed_id == MediaComment.user_id)
        .join(Media, Media.id == MediaComment.media_id)
        .where(Follows.follower_id == current_user_id)
        .order_by(desc(MediaComment.created_at))
        .limit(7)
    )

    comments = await session.execute(stmt)

    comments_data = comments.mappings().all()

    return comments_data


async def get_following_users_reviews(current_user_id: int, session: AsyncSession):
    """
    Retorna os útimos avaliacoes de usuários seguidos.

    Args:
        current_user_id (int): usuário logado.
        session (AsyncSession): sessão do banco de dados ativa.
    """

    stmt = (
        select(
            Review.user_id.label("user_id"),
            Review.score.label("score"),
            Media.title.label("media_title"),
            Media.id.label("media_id"),
            Media.poster_url.label("media_poster_url"),
        )
        .join(Follows, Follows.followed_id == Review.user_id)
        .join(Media, Media.id == Review.media_id)
        .where(Follows.follower_id == current_user_id)
        .order_by(desc(Review.created_at))
        .limit(7)
    )

    reviews = await session.execute(stmt)

    reviews_data = reviews.mappings().all()

    return reviews_data
