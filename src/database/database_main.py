from typing import AsyncGenerator

from aioredis import ConnectionPool, Redis
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.config import DATABASE_CONNECTION, REDIS_URL


class Base(DeclarativeBase):
    pass


engine = create_async_engine(DATABASE_CONNECTION)
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
