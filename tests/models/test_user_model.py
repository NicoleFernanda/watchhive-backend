from dataclasses import asdict

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.user_model import User


def test_create_user(session: Session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(username='alice', password='secret', email='teste@test')

        session.add(new_user)
        session.commit()

        user = session.scalar(select(User).where(User.username == 'alice'))

    assert asdict(user) == {
        'id': 1,
        'username': 'alice',
        'password': 'secret',
        'email': 'teste@test',
        'created_at': time,
        'updated_at': time,
    }
