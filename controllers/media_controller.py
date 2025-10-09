from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from controllers.user_controller import validate_user
from exceptions.record_not_found_error import RecordNotFoundError
from models.media_model import Genre, Media
from models.review_model import Review


async def get_media(media_id: int, session: AsyncSession):
    """
    Método retorna um post específico.

    Args:
        media_id (int): id do filme ou série.
        session (AsyncSession): sessão ativa do banco de dados.
    """
    return await existing_media(media_id, session)


async def get_random_medias(genre_id: int, movie: bool, session: AsyncSession):
    """
    Retorna vinte filmes aleatórios baseado num gênero específico.

    Args:
        genre_id (int): gênero a ser buscado.
        movie (bool): infoma se é filme ou não.
    """

    media_type = 'filme' if movie else 'série'

    medias = await session.scalars(
        select(Media)
        .join(Media.genres) 
        .where(
            Genre.id == genre_id,  # Filtra pelo gênero
            Media.media_type == media_type # Filtra pelo tipo ('filme' ou 'série')
        )
        .order_by(func.random())
        .limit(20)
    )

    return medias


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
    
    media.average_score = await get_average_score(media.id, session)

    return media


async def get_average_score(media_id: int, session) -> float:
    """
    Retorna a média das avaliações da mídia.
    """
    stmt = select(func.avg(Review.score)).where(Review.media_id == media_id)
    
    # 2. Executa a consulta na sessão assíncrona
    # Awaita o resultado
    result = await session.execute(stmt)
    
    # 3. Extrai o valor da média
    # O .scalar_one_or_none() retorna o primeiro (e único) valor escalar
    # (a média calculada) ou None se o resultado estiver vazio.
    average_score = result.scalar_one_or_none()
    
    # 4. Trata o caso em que não há avaliações
    # Se average_score for None (mídia sem reviews), retorna 0.0
    return average_score if average_score is not None else 0.0
