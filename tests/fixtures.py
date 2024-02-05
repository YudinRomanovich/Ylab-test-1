import asyncio

import pytest
from conftest import engine_test
from httpx import AsyncClient
from src.database.database_main import Base
from src.main import app


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def ac():
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac


@pytest.fixture(scope='session')
def menu_post() -> dict[str, str]:
    return {
        'title': 'My menu 1',
        'description': 'My menu description 1'
    }


@pytest.fixture(scope='session')
def menu_patch() -> dict[str, str]:
    return {
        'title': 'My updated menu 1',
        'description': 'My updated menu description 1'
    }


@pytest.fixture(scope='session')
def submenu_post() -> dict[str, str]:
    return {
        'title': 'My submenu 1',
        'description': 'My submenu description 1'
    }


@pytest.fixture(scope='session')
def submenu_patch() -> dict[str, str]:
    return {
        'title': 'My updated submenu 1',
        'description': 'My updated submenu description 1'
    }


@pytest.fixture(scope='session')
def dish_post() -> dict[str, str]:
    return {
        'title': 'My dish 1',
        'description': 'My dish description 1',
        'price': '12.50',
    }


@pytest.fixture(scope='session')
def dish_second_post() -> dict[str, str]:
    return {
        'title': 'My dish 2',
        'description': 'My dish description 2',
        'price': '13.50',
    }


@pytest.fixture(scope='session')
def dish_patch() -> dict[str, str]:
    return {
        'title': 'My updated dish 1',
        'description': 'My updated dish description 1',
        'price': '14.50',
    }
