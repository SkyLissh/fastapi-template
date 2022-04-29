from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Column, DateTime
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import as_declarative
from sqlalchemy.sql import func
from sqlalchemy_utils import UUIDType


@as_declarative()
class Base:
    id: UUID = Column(UUIDType(), primary_key=True, default=uuid4())
    created_at: datetime = Column(DateTime, server_default=func.now())
    update_at: datetime = Column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"
