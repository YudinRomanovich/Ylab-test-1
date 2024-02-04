from typing import AsyncGenerator

from aioredis import ConnectionPool, Redis
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from config import DATABASE_CONNECTION, REDIS_URL

metadata = MetaData()


class Base(DeclarativeBase):
    pass


engine = create_async_engine(DATABASE_CONNECTION)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


def create_redis():
    return ConnectionPool.from_url(REDIS_URL)


pool = create_redis()


def get_redis():
    return Redis(connection_pool=pool)
