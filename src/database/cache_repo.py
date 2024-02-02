import pickle

from aioredis import Redis
from fastapi import Depends

from database.database import get_redis
from database.models import Menu

from config import (
    EXPIRE,
    MENU_URL,
    MENUS_URL,
)

class CacheRepository:

    def __init__(
        self,
        cacher: Redis = Depends(get_redis)
    ) -> None:
        self.cacher = cacher

    async def delete_cache_by_mask(
        self,
        pattern: str,
    ) -> None:
        for key in await self.cacher.keys(pattern + '*'):
            await self.cacher.delete(key)

    async def set_all_menus_cache(self, menu_data: list[Menu]) -> None:
        await self.cacher.set(
            MENUS_URL,
            pickle.dumps(menu_data),
            ex=EXPIRE,
        )

    async def get_all_menus_cache(self) -> list[Menu] | None:
        cache = await self.cacher.get(MENUS_URL)
        if cache:
            menu_data = pickle.loads(cache)
            return menu_data
        return None


    async def set_menu_cache(self, menu_data: Menu) -> None:
        await self.cacher.set(
            MENU_URL.format(menu_id=str(menu_data.id)),
            pickle.dumps(menu_data),
            ex=EXPIRE,
        )

    async def get_menu_cache(self, menu_id: str) -> Menu | None:
        cache = await self.cacher.get(MENU_URL.format(menu_id=menu_id))
        if cache:
            menu_data = pickle.loads(cache)
            return menu_data
        return None


    async def create_update_menu_cache(self, menu_data: Menu) -> None:
        await self.delete_all_menu_cache()
        await self.cacher.set(
            MENU_URL.format(menu_id=str(menu_data.id)),
            pickle.dumps(menu_data),
            ex=EXPIRE,
        )

    async def delete_all_menu_cache(self) -> None:
        await self.cacher.delete(MENUS_URL)

    async def delete_menu_cache(self, menu_id: str) -> None:
        await self.delete_cache_by_mask(
            MENU_URL.format(menu_id=menu_id),
        )
        await self.delete_all_menu_cache()