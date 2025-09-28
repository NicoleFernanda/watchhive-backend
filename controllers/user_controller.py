from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from exceptions.business_error import BusinessError
from exceptions.permission_error import PermissionError
from exceptions.record_not_found_error import RecordNotFoundError
from models.user_list_model import ListType, UserList
from models.user_model import User
from security import get_password_hash


async def create_user(username: str, email: str, password: str, session: AsyncSession):
    """
    Método para criação de um usuário novo no banco de dados.
    Além disso, as listas desse usuário já são criadas.

    Args:
        username (str): username do usuário.
        email (str): email do usuário.
        password (str): senha do usuário.
        session (AsyncSession): sessão do banco de dados ativa.

    Raises:
        BusinessError: caso o email ou username já estiverem em uso.

    Returns:
        user (User): usuário adicionado no banco de dados.
    """
    user = await session.scalar(
        select(User).where(
            (User.username == username) | (User.email == email)
        )
    )

    if user:
        if user.username == username:
            raise BusinessError('Username em uso.')
        elif user.email == email:
            raise BusinessError('Email em uso.')

    user = User(
        username=username, password=get_password_hash(password), email=email
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    await create_lists(user.id, session)

    return user


async def get_all_users(limit: int, offset: int, session: AsyncSession):
    """
    Método para retornar todos os usuários do banco com suporte a paginação.
    Exemplo: cada página retorna dois usuários e preciso ignorar os dois anteriores.

    Args:
        limit (int): número máximo de usuários a serem retornados.
        offset (int): número de registros a serem ignorados antes de começar a retornar os resultados.
        session (AsyncSession): sessão do banco de dados ativa.

    Returns:
        list[User]: lista de usuários.
    """
    users = await session.scalars(select(User).limit(limit).offset(offset))

    return users


async def update_user(
        current_user: User,
        user_id: int,
        username: str,
        email: str,
        password: str,
        session: AsyncSession
):
    """
    Método para atualização total de um usuário.

    Args:
        current_user(User): usuário logado.
        user_id (int): usuário a ser "mexido", passado pela url.
        username (str): username do usuário.
        email (str): email do usuário.
        password (str): senha do usuário.
        session (AsyncSession): sessão do banco de dados ativa.

    Raises:
        BusinessError: caso o email ou username já estiverem em uso.

    Returns:
        user (User): usuário adicionado no banco de dados.
    """
    validate_user(logger_user_id=current_user.id, user_id_passed=user_id)

    try:
        current_user.username = username
        current_user.password = get_password_hash(password)
        current_user.email = email
        await session.commit()
        await session.refresh(current_user)

        return current_user

    except IntegrityError:
        raise BusinessError('Username ou Email já existe.',
    )


async def delete_user(current_user, user_id: int, session: AsyncSession):
    """
    Apaga um usuário do banco de dados.

    Args:
        current_user(User): usuário logado.
        user_id (int): usuário a ser "mexido", passado pela url.
        session (AsyncSession): sessão do banco de dados ativa.

    Raises:
        PermissionError: caso o usuário a ser utilizado em operações não seja o mesmo logado.
            No caso, quando alguém está tentando alterar o perfil de outra pessoa.
    """

    validate_user(logger_user_id=current_user.id, user_id_passed=user_id)

    await session.delete(current_user)  # TODO AAA: provavelmente, alguma lógita terá de ser implemntada daqui um tempo
    await session.commit()


async def get_user(user_id: int, session: AsyncSession):
    """
    Retorna um usuário específico do banco.

    Args:
        user_id (int): id do usuário.

    Raises:
        RecordNotFoundError: caso não exista um usuário específico com aquele id.

    Returns:
        user (User): usuário retornado.
    """

    db_user = await existing_user(user_id, session)

    return db_user


def validate_user(logger_user_id: int, user_id_passed: int):
    """
    Método responsável por validar se o usuário a ser "alterado" nas operações
    é o mesmo que está logado.

    Args:
        logger_user_id (int): id do usuário logado.
        user_id_passed (int): id passado na url.

    Raises:
        PermissionError: caso o usuário a ser utilizado em operações não seja o mesmo logado.
            No caso, quando alguém está tentando alterar o perfil de outra pessoa.
    """
    if logger_user_id != user_id_passed:
        raise PermissionError('Usuário não possui permissão para editar informações de outro usuário.')


async def existing_user(user_id: int, session):
    """
    Método responsável por retornar um usuário ativo da plataforma.

    Args:
        session (AsyncSession): sessão ativa do banco
        user_id (int): usuário.

    Raises:
        RecordNotFoundError: caso o usuário não exista
    """

    user = await session.scalar(select(User).where((User.id == user_id)))

    if not user:
        raise RecordNotFoundError('Usuário não encontrado.')
    
    return user


async def create_lists(user_id: int, session: AsyncSession):
    """
    Método para crias as listas quero asssitir e assistidos
    """

    lists_to_create = [
        UserList(user_id=user_id, name=ListType.WATCHED),
        UserList(user_id=user_id, name=ListType.TO_WATCH),
    ]

    session.add_all(lists_to_create)
    await session.commit()
