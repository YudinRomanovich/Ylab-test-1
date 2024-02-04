import asyncio
import pytest

from typing import AsyncGenerator
from httpx import AsyncClient

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from src.database.database import get_async_session, metadata
from src.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER
from src.main import app


# DATABASE TEST
DATABASE_URL_TEST = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


# CREATE ENGINE
engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
metadata.bind = engine_test

@pytest.fixture(scope="session")
async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
def menu_post() -> dict[str, str]:
    return {
        'title': 'My menu 1',
        'description': 'My menu description 1'
    }


@pytest.fixture(scope="session")
def menu_patch() -> dict[str, str]:
    return {
        'title': 'My updated menu 1',
        'description': 'My updated menu description 1'
    }


@pytest.fixture(scope="session")
def submenu_post() -> dict[str, str]:
    return {
        'title': 'My submenu 1',
        'description': 'My submenu description 1'
    }


@pytest.fixture(scope="session")
def submenu_patch() -> dict[str, str]:
    return {
        'title': 'My updated submenu 1',
        'description': 'My updated submenu description 1'
    }


@pytest.fixture(scope="session")
def dish_post() -> dict[str, str]:
    return {
        'title': 'My dish 1',
        'description': 'My dish description 1',
        'price': '12.50',
    }


@pytest.fixture(scope="session")
def dish_second_post() -> dict[str, str]:
    return {
        'title': 'My dish 2',
        'description': 'My dish description 2',
        'price': '13.50',
    }


@pytest.fixture(scope="session")
def dish_patch() -> dict[str, str]:
    return {
        'title': 'My updated dish 1',
        'description': 'My updated dish description 1',
        'price': '14.50',
    }