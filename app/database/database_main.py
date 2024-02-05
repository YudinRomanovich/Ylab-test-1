from typing import AsyncGenerator

from aioredis import ConnectionPool, Redis
from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER, REDIS_URL
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# metadata = MetaData()


class Base(DeclarativeBase):
    pass


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


def create_redis():
    return ConnectionPool.from_url(REDIS_URL)


pool = create_redis()


def get_redis():
    return Redis(connection_pool=pool)
