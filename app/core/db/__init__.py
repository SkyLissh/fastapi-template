from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Column, DateTime, func
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import as_declarative
from sqlalchemy_utils import UUIDType


@as_declarative()
class Base:
    id: UUID = Column(UUIDType(binary=False), primary_key=True, default=uuid4)
    created_at: datetime = Column(DateTime, default=func.current_timestamp())
    updated_at: datetime = Column(
        DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp()
    )

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"
