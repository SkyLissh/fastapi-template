from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

if not settings.SQLALCHEMY_DATABASE_URI:
    raise Exception("SQLALCHEMY_DATABASE_URI must be set")

engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI, echo=True, future=True)
SessionLocal = sessionmaker(
    engine,
    autocommit=False,
    autoflush=False,
    class_=AsyncSession,
    expire_on_commit=False,
)
