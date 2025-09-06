from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from jwt import encode
from pwdlib import PasswordHash

pwd_context = PasswordHash.recommended()

SECRET_KEY = 'your_secret_key'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = 'HS256'


def create_access_token(data: dict):
    """
    Método para criar o token de acess.
    Args:
        data: dados que serão assinados.
    """
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})
    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hased_password: str):
    return pwd_context.verify(plain_password, hased_password)
