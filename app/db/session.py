from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

if not settings.SQLALCHEMY_DATABASE_URI:
    raise Exception("SQLALCHEMY_DATABASE_URI must be set")

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, echo=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
