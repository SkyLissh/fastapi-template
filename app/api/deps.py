from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import SessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    db: AsyncSession | None = None

    try:
        db = SessionLocal()
        yield db
    finally:
        if db is not None:
            await db.close()
