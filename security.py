from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from models.user_model import User
from settings import settings

pwd_context = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')


def create_access_token(data: dict):
    """
    Cria um token JWT de acesso com tempo de expiração definido.

    Args:
        data (dict): Dados a serem incluídos no payload do token e que ser'ao assinados.
            (ex.: {"sub": email_do_usuario}).

    Returns:
        str: Token JWT assinado.
    """
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})
    encoded_jwt = encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def get_password_hash(password: str):
    """
    Gera o hash de uma senha em texto plano.

    Args:
        password (str): Senha em texto plano.

    Returns:
        str: Senha criptografada (hash).
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hased_password: str) -> bool:
    """
    Verifica se uma senha em texto plano corresponde ao hash armazenado.

    Args:
        plain_password (str): Senha em texto plano.
        hased_password (str): Senha já criptografada.

    Returns:
        bool: True se a senha for válida, False caso contrário.
    """
    return pwd_context.verify(plain_password, hased_password)


async def get_current_user(
    session: AsyncSession = Depends(get_session),
    token: str = Depends(oauth2_scheme),
):
    """
    Recupera o usuário autenticado a partir do token JWT.

    Args:
        session (Session): Sessão do banco de dados.
        token (str): Token JWT obtido do cabeçalho de autorização.

    Raises:
        HTTPException: Se o token for inválido, expirado ou não contiver 'sub'.

    Returns:
        User: Instância do usuário autenticado.
    """
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Não foi possível validar credenciais.',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        subject_email = payload.get('sub')

        if not subject_email:
            raise credentials_exception

    except DecodeError:
        raise credentials_exception

    user = await session.scalar(
        select(User).where(User.email == subject_email)
    )

    if not user:
        raise credentials_exception

    return user
