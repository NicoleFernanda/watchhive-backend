from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Genre(Base):
    __tablename__ = "genre"

    id: Mapped[int] = mapped_column(init=True, primary_key=True)
    name: Mapped[str]
