from aioredis import ConnectionPool, Redis
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData

from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER, REDIS_URL

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

metadata = MetaData()


class Base(DeclarativeBase):
    pass


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

def create_redis():
    return ConnectionPool.from_url(REDIS_URL)


pool = create_redis()


def get_redis():
    return Redis(connection_pool=pool)