from contextlib import contextmanager
from datetime import datetime

import factory
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, event
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from database import get_session
from main import app
from models.base import Base
from models.forum_comment_model import ForumMessage
from models.forum_group_model import ForumGroup
from models.forum_participant_model import ForumParticipant
from models.media_comment_model import MediaComment
from models.media_model import Media
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


@pytest_asyncio.fixture
async def session():
    """
    Fornece uma sessão temporária do banco de dados em memória.

    Cria um engine SQLite em memória, todas as tabelas, fornece uma sessão ativa para testes e,
    ao final do teste, remove todas as tabelas, garantindo isolamento entre testes.
    """
    engine = create_async_engine(
        'sqlite+aiosqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,  # executa nas mesmas threads
    )  # cria conexão

    # cria tabelas de forma sincrona, pois não faz sentido crias tabelas de forma assincrona.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


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


# user
@pytest_asyncio.fixture
async def user(session: AsyncSession):
    password = 'beelover'
    user = UserFactory(password=get_password_hash(password))
    session.add(user)
    await session.commit()
    await session.refresh(user)

    user.clean_password = password  # monkey patch

    return user


@pytest_asyncio.fixture
async def other_user(session):
    password = 'beehater'
    user = UserFactory(password=get_password_hash(password))

    session.add(user)
    await session.commit()
    await session.refresh(user)

    user.clean_password = password

    return user


# forum
@pytest_asyncio.fixture
async def forum_group(session: AsyncSession):
    post = ForumGroupFactory()
    session.add(post)
    await session.commit()
    await session.refresh(post)

    return post


@pytest_asyncio.fixture
async def forum_participant(session: AsyncSession, forum_group):
    participant = ForumParticipantFactory()
    session.add(participant)
    await session.commit()
    await session.refresh(participant)
    await session.refresh(forum_group)

    return participant


@pytest_asyncio.fixture
async def forum_message(session: AsyncSession):
    comment = ForumMessageFactory()
    session.add(comment)
    await session.commit()
    await session.refresh(comment)

    return comment


# media
@pytest_asyncio.fixture
async def media(session: AsyncSession):
    media = MediaFactory()

    session.add(media)
    await session.commit()
    await session.refresh(media)

    return media


@pytest_asyncio.fixture
async def media_comment(session: AsyncSession):
    media_comment = MediaCommentFactory()

    session.add(media_comment)
    await session.commit()
    await session.refresh(media_comment)

    return media_comment


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


class UserFactory(factory.Factory):
    class Meta:
        model = User  # toda vez que chama, cria um novo usuario

    username = factory.Sequence(lambda n: f'test{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}123')


class ForumGroupFactory(factory.Factory):
    class Meta:
        model = ForumGroup  # toda vez que chama, cria um novo

    title = factory.Sequence(lambda n: f'title{n}')
    content = factory.Sequence(lambda n: f'content{n}')
    user_id = 1


class ForumParticipantFactory(factory.Factory):
    class Meta:
        model = ForumParticipant  # toda vez que chama, cria um novo

    forum_group_id = 1
    user_id = 1


class ForumMessageFactory(factory.Factory):
    class Meta:
        model = ForumMessage  # toda vez que chama, cria um novo

    content = factory.Sequence(lambda n: f'content{n}')
    user_id = 2
    forum_group_id = 1


class MediaFactory(factory.Factory):
    class Meta:
        model = Media  # toda vez que chama, cria um novo

    id_themoviedb = factory.Sequence(lambda n: 1000 + n)
    id_imdb = factory.Sequence(lambda n: f'tt{1000000 + n}')
    title = factory.Sequence(lambda n: f'Movie Title {n}')
    original_title = factory.Sequence(lambda n: f'Original Title {n}')
    description = factory.Faker('paragraph', nb_sentences=3)
    dt_launch = factory.Faker('date_object')
    original_language = factory.Iterator(['en', 'pt', 'es', 'fr'])
    media_type = factory.Iterator(['movie', 'series', 'documentary'])
    poster_url = factory.Faker('image_url')
    popularity = factory.Faker('pyfloat', left_digits=2, right_digits=2, positive=True)
    vote_average = factory.Faker('pyfloat', left_digits=1, right_digits=1, positive=True)
    vote_count = factory.Faker('random_int', min=0, max=10000)
    adult = factory.Faker('boolean')


class MediaCommentFactory(factory.Factory):
    class Meta:
        model = MediaComment  # toda vez que chama, cria um novo

    media_id = 1
    user_id = 1
    content = factory.Sequence(lambda n: f'content{n}')
    