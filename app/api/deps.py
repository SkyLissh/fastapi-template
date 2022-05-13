from typing import Generator, Optional

from sqlalchemy.orm import Session

from app.db.session import SessionLocal


def get_db() -> Generator[Session, None, None]:
    db: Optional[Session] = None

    try:
        db = SessionLocal()
        yield db
    finally:
        if db is not None:
            db.close()
