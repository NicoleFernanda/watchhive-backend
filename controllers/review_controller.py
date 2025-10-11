from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from controllers.media_controller import existing_media
from controllers.user_list_controller import add_to_list_to_watched
from exceptions.business_error import BusinessError
from models.media_model import Media
from models.review_model import Review


async def create_review(media_id: int, user_id: int, score: int, session: AsyncSession) -> Media:
    """
    Método responsável por criar um review.

    Args:
        media_id (int): id do filme ou série.
        user_id (int): id do usuário ativo.

        session (AsyncSession): sessão ativa do banco.

    Raises:
        RecordNotFoundError: caso a mídia pesquisada não seja encontrada.
    """
    media = await existing_media(media_id, session)

    check_score_value(score)

    review = await existing_review(user_id, media_id, session)

    if review:
        review.score = score

    else:
        # create review
        review = Review(
            user_id=user_id,
            media_id=media_id,
            score=score
        )

        session.add(review)
        await add_to_list_to_watched(user_id, media_id, session)

    await session.commit()
    await session.refresh(review)

    return review


async def existing_review(user_id: int, media_id: int, session: AsyncSession):
    """
    Método retorna um review, caso já esteja criado.

    Args:
        user_id (int): id do usuário ativo.
        media_id (int): id do filme ou série.
        session (AsyncSession): sessão ativa do banco de dados.
    """

    review = await session.scalar(
        select(Review)
        .where((Review.user_id == user_id) & (Review.media_id == media_id))
    )

    return review


def check_score_value(score: int):
    """
    Checa para ver o valor do score está dentro do padrão

    Args:
        score (int): valor da avalização, de 1 a 5.
    
    Raises: 
        BusinessError: caso o valor esteja abaixo ou acima.
    """

    if score > 5 or score < 1:
        raise BusinessError('A zavalização deve ser entre 1 e 5.')
