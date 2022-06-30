from typing import AsyncGenerator

import pytest
from httpx import AsyncClient

from app.core.config import settings
from app.main import app


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """
    HTTPX client for testing.
    """

    async with AsyncClient(
        app=app, base_url=f"http://test{settings.API_VERSION}"
    ) as client:
        yield client
