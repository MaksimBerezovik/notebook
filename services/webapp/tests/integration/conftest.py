from typing import AsyncGenerator
from typing import Iterable

import httpx
import pytest
from django.core.management import call_command

from alpha.settings import Settings
from project.asgi import application
from project.consts import TESTING_DB

settings = Settings()
TIMEOUT = 20


@pytest.fixture(scope="function")
async def asgi_client() -> AsyncGenerator[httpx.AsyncClient, None]:
    async with httpx.AsyncClient(
        app=application,
        base_url="http://asgi",
        timeout=TIMEOUT,
    ) as client:
        yield client


@pytest.fixture(scope="function")
async def web_client() -> AsyncGenerator[httpx.AsyncClient, None]:
    async with httpx.AsyncClient(
        base_url=settings.TEST_SERVICE_URL,
        timeout=TIMEOUT,
    ) as client:
        yield client


@pytest.fixture(
    autouse=True,
    scope="session",
)
def migrate_db() -> Iterable[None]:
    if settings.MODE_TESTING:
        TESTING_DB.unlink(missing_ok=True)
        call_command("migrate", "--database=testing")
    yield
