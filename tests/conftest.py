from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine, event
from sqlalchemy.orm import Session

from database import get_session
from main import app
from models.base import Base
from models.user_model import User
from security import get_password_hash
from settings import Settings


@pytest.fixture
def client(session):
    """
    Nesse caso, no lugar de chamar o get_session com os dados do meu banco dem produção,
    ele chama uma função que eu escolhi. Portanto nos testes, eu passo a utilizar o banco
    em memória - que é resetado a cada teste.
    """
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    """
    Fornece uma sessão temporária do banco de dados em memória.

    Cria um engine SQLite em memória, todas as tabelas, fornece uma sessão ativa para testes e,
    ao final do teste, remove todas as tabelas, garantindo isolamento entre testes.
    """
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,  # executa nas mesmas threads
    )  # cria conexão

    Base.metadata.create_all(engine)

    with Session(engine) as session:  # cria uma sessão de troca entre o banco e o codigo
        yield session

    Base.metadata.drop_all(engine)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@contextmanager
def _mock_db_time(*, model, time=datetime(2025, 9, 4)):
    """
    Toda vez que uma instância for inserida no banco,
    executa o hook `fake_time_hook` antes de inseri-lo.
    O hook permite inspecionar ou modificar a instância antes que ela seja salva no banco.

    Args:
        model: classe do SQLAlchemy a ser monitorada
        time: datetime "mockado" que será usado nos testes
    """
    def fake_time_hook(mapper, conection, target):
        """
        Antes de inserir o dado, executa essa ação.
        Args:
            target: objeto do modelo que sera inserido
            connection: conexão (sqlite)
            mapper: modelo
        """
        if hasattr(target, 'created_at'):
            target.created_at = time
        if hasattr(target, 'updated_at'):
            target.updated_at = time

    event.listen(model, 'before_insert', fake_time_hook)

    yield time

    event.remove(model, 'before_insert', fake_time_hook)


# objetos no banco
@pytest.fixture
def user(session):
    password = 'beelover'
    user = User(username='bee', email='bee@test.com', password=get_password_hash(password))
    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = password  # monkey patch

    return user


@pytest.fixture
def token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password}
    )

    return response.json()['access_token']


@pytest.fixture
def settings():
    return Settings()
