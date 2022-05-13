from typing import AsyncGenerator, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import SessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    db: Optional[AsyncSession] = None

    try:
        db = SessionLocal()
        yield db
    finally:
        if db is not None:
            await db.close()
