from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)  # o banco quem gerencia o id
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime]

    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
