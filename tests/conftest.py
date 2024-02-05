import os
import sys
from typing import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, os.path.abspath('/app'))
# from app.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

DB_HOST = 'db'
DB_PORT = 5432
DB_NAME = 'postgres'
DB_USER = 'postgres'
DB_PASS = 'postgres'

# DATABASE TEST
DATABASE_URL_TEST = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# CREATE ENGINE
engine_test = create_async_engine(DATABASE_URL_TEST)

async_session_maker = sessionmaker(autocommit=False, autoflush=False,
                                   bind=engine_test, class_=AsyncSession)

pytest_plugins = 'tests.fixtures'


@pytest.fixture(scope='session')
async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
