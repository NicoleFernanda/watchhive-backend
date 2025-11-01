from typing import List

from sqlalchemy import case, desc, func, literal_column, select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from exceptions.record_not_found_error import RecordNotFoundError
from models.media_model import Genre, Media, media_genre
from models.review_model import Review
from models.user_list_model import ListType, UserList, UserListMedia


async def get_media(media_id: int, current_user_id: int, session: AsyncSession):
    """
    Método retorna um post específico.

    Args:
        media_id (int): id do filme ou série.
        session (AsyncSession): sessão ativa do banco de dados.
    """
    return await existing_media(media_id, session, current_user_id)


async def get_random_medias(genre_id: int, movie: bool, session: AsyncSession, limit: int = 20, offset: int = 0) -> List[Media]:
    """
    Retorna vinte filmes aleatórios baseado num gênero específico.

    Args:
        genre_id (int): gênero a ser buscado.
        movie (bool): infoma se é filme ou não.
        offset (int): Número de registros a pular (paginação).
        limit (int): Número máximo de registros a retornar (paginação).
    """

    media_type = 'filme' if movie else 'série'

    medias = await session.scalars(
        select(Media)
        .join(Media.genres)
        .where(
            Genre.id == genre_id,  # Filtra pelo gênero
            Media.media_type == media_type  # Filtra pelo tipo ('filme' ou 'série')
        )
        .order_by(func.random())
        .limit(limit)
        .offset(offset)
    )

    return medias


async def search_medias_by_title(
    search_term: str,
    session: AsyncSession,
    offset: int = 0,
    limit: int = 50,
) -> List[Media]:
    """
    Busca mídias cujo título contenha o termo de pesquisa (case-insensitive) 
    e aplica paginação.

    Args:
        search_term (str): O termo de pesquisa (ex: 'ba').
        session (AsyncSession): A sessão ativa do banco.
        offset (int): Número de registros a pular (paginação).
        limit (int): Número máximo de registros a retornar (paginação).

    Returns:
        List[Media]: Uma lista de objetos Media que correspondem à pesquisa.
    """

    # pesquisa com curingas (%) - tipo o like no sql
    like_term = f"%{search_term}%"

    stmt = (
        select(Media)
        .where(Media.title.ilike(like_term))  # .ilike() para busca case-insensitive
        .order_by(Media.title)  # ordena por título para melhor usabilidade (ordem alfabética)
        .offset(offset)
        .limit(limit)
    )

    medias = await session.scalars(stmt)

    return medias


async def show_medias_by_genre_page(
    genre_id: int,
    movie: bool,
    limit: int,
    offset: int,
    session=AsyncSession,
) -> List[Media]:
    """
    Retorna os filmes ou séries aleatórios baseado num gênero específico.
    Utiliza a função get_random_medias() para auxiliar.

    Args:
        genre_id (int): gênero a ser buscado.
        movie (bool): infoma se é filme ou não.
        offset (int): Número de registros a pular (paginação).
        limit (int): Número máximo de registros a retornar (paginação).
    """

    media_type = 'filme' if movie else 'série'

    medias = await session.scalars(
        select(Media)
        .join(Media.genres)
        .where(
            Genre.id == genre_id,  # Filtra pelo gênero
            Media.media_type == media_type  # Filtra pelo tipo ('filme' ou 'série')
        )
        .order_by(desc(Media.popularity))
        .limit(limit)
        .offset(offset)
    )

    return medias


async def existing_media(media_id: int, session: AsyncSession, current_user_id: int = None,) -> Media:
    """
    Método responsável por validar se o filme ou série existe e, caso seja verdade, o retorne.

    Args:
        media_id (int): id do filme ou série.
        session (AsyncSession): sessão ativa do banco.
        current_user_id (int): id do usuário logado

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
    media.vote_count = await get_votes_count(media.id, session)

    if current_user_id:
        review = await session.scalar(
            select(Review)
            .where((Review.user_id == current_user_id) & (Review.media_id == media_id))
        )

        media_in_list = await session.scalar(
            select(UserListMedia)
            .join(UserList, UserListMedia.user_list_id == UserList.id)
            .where(
                UserList.user_id == current_user_id,
                UserList.name == ListType.TO_WATCH,
                UserListMedia.media_id == media_id
            )
        )
        media.to_watch_list = True if media_in_list else False
        media.user_review = review.score if review else None

    return media


async def get_best_rated_medias(
    session: AsyncSession,
    limit: int,
):
    """
    Retorna uma lista de mídias (filmes ou séries) ordenadas pela pontuação média mais alta.

    Args:
        media_id (int): id do filme ou série.
        session (AsyncSession): sessão ativa do banco.
    """
    # coluna para calcular
    average_score = func.avg(Review.score).label("average_score")

    # vote_count = func.count(Review.id).label("vote_count")

    stmt = (
        select(
            Media
        )
        .join(Review, Media.id == Review.media_id)
        .group_by(Media.id)
        # .having(vote_count >= 5) # mínimo de votos
        .order_by(desc(average_score))
        .limit(limit)
    )

    result = await session.execute(stmt)

    medias: List[Media] = result.scalars().all()

    return medias


async def get_recommended_medias(current_user_id: int, limit: int, session: AsyncSession):
    """
    Retorna filmes recomedados a partir da última avaliação do usuário.
    A partir dos gêneros do último filme/série avaliado(a), retorna uma lista de mídias
    com as melhores médias de avaliações dos outros usuários da plataforma.

    Caso o usuário já tenha assistido, não é considerado.

    Args:
        current_user_id (int): id do usuário logado
        limit (int): limite de mídias
        session (AsyncSession): sessão ativa do banco
    """

    stmt_last_review = (
        select(Review.media_id)
        .where(Review.user_id == current_user_id)
        .order_by(desc(Review.created_at))
        .limit(1)
    ).cte("UltimaReview")

    stmt_generos = (
        select(media_genre.c.genre_id)
        .where(media_genre.c.media_id.in_(select(stmt_last_review.c.media_id)))
    ).cte("GenerosRecomendados")

    stmt_internal_rank = (
        select(
            Review.media_id.label("media_id"),
            func.avg(Review.score).label("internal_avg"),
            func.count(Review.id).label("internal_count")
        )
        .group_by(Review.media_id)
    ).cte("MediaDosFilmes")

    watched_user_list_id_stmt = (
        select(UserList.id)
        .where(
            (UserList.user_id == current_user_id) & 
            (UserList.name == ListType.WATCHED)
        )
    ).scalar_subquery()

    stm_already_seen = (
        select(UserListMedia.media_id.label("id"))
        .where(
            UserListMedia.user_list_id == watched_user_list_id_stmt
        )
    ).cte("MidiasAssistidas")

    final_select = (
        select(
            Media.id,
            Media.title,
            Media.poster_url,
        ) 
        # garante que apenas filmes com reviews sejam considerados
        .join(stmt_internal_rank, Media.id == stmt_internal_rank.c.media_id)
        .where(
            Media.id.in_(
                select(media_genre.c.media_id)
                .where(media_genre.c.genre_id.in_(select(stmt_generos.c.genre_id)))
            ),
            Media.id != select(stmt_last_review.c.media_id).scalar_subquery(),
            Media.id.notin_(select(stm_already_seen.c.id)),
        )
        .order_by(
            desc(stmt_internal_rank.c.internal_avg), 
        )
        .limit(limit)
    )

    result = await session.execute(final_select)

    recommended_medias_list = [
        {
            "id": row[0],
            "title": row[1],
            "poster_url": row[2]
        }
        for row in result.unique()
    ]

    return recommended_medias_list


async def get_average_score(media_id: int, session) -> float:
    """
    Retorna a média das avaliações da mídia.

    Args:
        media_id (int): id do filme ou série.
        session (AsyncSession): sessão ativa do banco.
    """
    stmt = select(func.avg(Review.score)).where(Review.media_id == media_id)

    result = await session.execute(stmt)

    average_score = result.scalar_one_or_none()

    # se for None (sem reviews), retorna zero
    return average_score if average_score is not None else 0.0


async def get_votes_count(media_id: int, session) -> int:
    """
    Retorna a quantidad de avaliações da mídia.

    Args:
        media_id (int): id do filme ou série.
        session (AsyncSession): sessão ativa do banco.
    """
    stmt = select(func.count(Review.id)).where(Review.media_id == media_id)

    result = await session.execute(stmt)

    vote_count = result.scalar_one_or_none()

    return vote_count if vote_count is not None else 0
