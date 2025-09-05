from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass

metadata_obj = MetaData()


class Base(MappedAsDataclass, DeclarativeBase):
    __mapper_args__ = {"eager_defaults": True}
    # means that a backend that supports RETURNING will usually make use of RETURNING with INSERT statements
    # in order to retrieve newly generated default values
