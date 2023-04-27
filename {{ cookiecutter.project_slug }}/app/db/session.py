from app.core.config import settings
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

if not settings.SQLALCHEMY_DATABASE_URI:
    raise Exception("SQLALCHEMY_DATABASE_URI must be set")

engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI, echo=True)
SessionLocal = async_sessionmaker(
    engine,
    autoflush=False,
    expire_on_commit=False,
)
