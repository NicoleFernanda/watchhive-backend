from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from controllers.media_controller import existing_media
from exceptions.business_error import BusinessError
from exceptions.permission_error import PermissionError
from exceptions.record_not_found_error import RecordNotFoundError
from models.user_list_model import ListType, UserList, UserListMedia
from models.user_model import User
from security import get_password_hash


async def add_to_list_to_watch(user_id: int, media_id: int, session: AsyncSession):
    """
    Adiciona um titúlo para a lista de filmes quero assistir.

    Args:
        user_id (int): usuário adicionando a lista.
        media_id (str): id da mídia
        session (AsyncSession): sessão do banco de dados ativa
        
    Raises:
        RecordNotFound: caso não exista mídia.
    """

    try: 
        existing_media(media_id, session)

        is_media_in_list = await existing_media_in_list(user_id, media_id, ListType.TO_WATCH, session)
            

        list = await session.scalar(
            select(UserList)
            .where((UserList.user_id == user_id) & (UserList.name == ListType.TO_WATCH))
        )

        media_in_list = UserListMedia(
            user_list_id=list.id,
            media_id=media_id
        )

        session.add(media_in_list)
        await session.commit()
        await session.refresh(media_in_list)
        await session.refresh(list)
    except IntegrityError:
        raise BusinessError('Título já adicionado a lista.')


async def add_to_list_to_watched(user_id: int, media_id: int, session: AsyncSession):
    """
    Adiciona um titúlo para a lista de filmes assistidos.

    Args:
        user_id (int): usuário adicionando a lista
        media_id (str): id da mídia
        session (AsyncSession): sessão do banco de dados ativa
        
    Raises:
        RecordNotFound: caso não exista mídia.
    """

    try: 
        existing_media(media_id, session)

        is_media_in_list = await existing_media_in_list(user_id, media_id, ListType.WATCHED, session)

        list = await session.scalar(
            select(UserList)
            .where((UserList.user_id == user_id) & (UserList.name == ListType.WATCHED))
        )

        media_in_list = UserListMedia(
            user_list_id=list.id,
            media_id=media_id
        )

        session.add(media_in_list)
        
    except IntegrityError:
        raise BusinessError('Título já adicionado a lista.')


async def existing_media_in_list(user_id: int, media_id: int, list_type: ListType, session: AsyncSession):
    """
    Verifica a existência de uma mídia (filme/série) específica na lista 
    de um usuário.

    Args:
        user_id (int): O ID do usuário dono da lista.
        media_id (int): O ID da mídia (filme/série) a ser verificada.
        list_type (str): O tipo da lista ('assistidos', 'quero_assistir', etc.).
        session (AsyncSession): Sessão assíncrona do banco de dados ativa.

    Returns:
        bool: Retorna True se a mídia for encontrada na lista, False caso contrário.
    """
    stmt = (
        select(UserListMedia)
        # JOIN para encontrar a UserList correta (pelo usuário e tipo)
        .join(UserList, UserListMedia.user_list_id == UserList.id)
        .where(
            UserList.user_id == user_id,
            UserList.name == list_type,
            UserListMedia.media_id == media_id
        )
    )

    result = await session.scalar(stmt)
    
    return result is not None
