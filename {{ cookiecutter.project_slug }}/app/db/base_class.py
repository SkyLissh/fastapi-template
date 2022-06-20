from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import as_declarative
from sqlalchemy.sql import func


@as_declarative()
class Base:
    id: UUID = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at: datetime = Column(DateTime, default=func.now())
    updated_at: datetime = Column(DateTime, default=func.now(), onupdate=func.now())

    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"
