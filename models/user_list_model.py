from datetime import datetime
from enum import Enum
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.media_model import Media

from .base import Base

class ListType(str, Enum):
    """Tipos de listas padrão de um usuário."""
    
    WATCHED = "assistidos" 
    TO_WATCH = "quero_assistir" 
    # FAVORITES = "favoritos" 


class UserList(Base):
    __tablename__ = "user_list"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    name: Mapped[ListType]


class UserListMedia(Base):
    __tablename__ = "user_list_media"

    user_list_id: Mapped[int] = mapped_column(
        ForeignKey('user_list.id', ondelete='CASCADE'), 
        primary_key=True
    )

    media_id: Mapped[int] = mapped_column(
        ForeignKey('media.id', ondelete='CASCADE'), 
        primary_key=True
    )

    added_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )

    user_list: Mapped['UserList'] = relationship(backref="list_media", init=False) 
    media: Mapped['Media'] = relationship(init=False)
