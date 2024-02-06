from typing import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.config import DATABASE_CONNECTION

# CREATE ENGINE
engine_test = create_async_engine(DATABASE_CONNECTION)

async_session_maker = sessionmaker(autocommit=False, autoflush=False,
                                   bind=engine_test, class_=AsyncSession)

pytest_plugins = 'tests.fixtures'


@pytest.fixture(scope='session')
async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
