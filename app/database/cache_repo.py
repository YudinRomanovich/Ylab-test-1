import pickle

from aioredis import Redis
from fastapi import Depends
from src.config import (
    DISH_URL,
    DISHES_URL,
    EXPIRE,
    MENU_INFO_URL,
    MENU_URL,
    MENUS_URL,
    SUBMENU_URL,
    SUBMENUS_URL,
)
from src.database.database_main import get_redis
from src.database.models import Dish, Menu, Submenu


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

    async def get_specific_menu_info_cache(self, menu_id: str) -> Menu | None:
        cache = await self.cacher.get(MENU_INFO_URL.format(menu_id=menu_id))
        if cache:
            menu_data = pickle.loads(cache)
            return menu_data
        return None

    async def set_specific_menu_info_cache(self, menu_data: Menu) -> None:
        await self.cacher.set(
            MENU_INFO_URL.format(menu_id=str(menu_data.id)),
            pickle.dumps(menu_data),
            ex=EXPIRE
        )

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

    async def set_all_submenus_cache(
            self,
            menu_id: str,
            submenu_data: list[Submenu]
    ) -> None:
        await self.cacher.set(
            SUBMENUS_URL.format(menu_id=menu_id),
            pickle.dumps(submenu_data),
            ex=EXPIRE,
        )

    async def get_all_submenus_cache(
            self,
            menu_id: str
    ) -> list[Submenu] | None:
        cache = await self.cacher.get(SUBMENUS_URL.format(menu_id=menu_id))
        if cache:
            submenu_data = pickle.loads(cache)
            return submenu_data
        return None

    async def set_submenu_cache(
            self,
            menu_id: str,
            submenu_data: Submenu
    ) -> None:
        await self.cacher.set(
            SUBMENU_URL.format(
                menu_id=menu_id,
                submenu_id=str(submenu_data.id)),
            pickle.dumps(submenu_data),
            ex=EXPIRE,
        )

    async def get_submenu_cache(
            self,
            menu_id: str,
            submenu_id: str
    ) -> Submenu | None:
        cache = await self.cacher.get(SUBMENU_URL.format(
            menu_id=menu_id,
            submenu_id=submenu_id)
        )
        if cache:
            submenu_data = pickle.loads(cache)
            return submenu_data
        return None

    async def update_submenu_cache(
            self,
            menu_id: str,
            submenu_data: Submenu
    ) -> None:

        await self.delete_all_submenu_cache(str(submenu_data.menu_id))
        await self.set_submenu_cache(
            menu_id=menu_id,
            submenu_data=submenu_data
        )

    async def delete_all_submenu_cache(self, menu_id: str) -> None:
        await self.cacher.delete(SUBMENUS_URL.format(menu_id=menu_id))

    async def delete_submenu_cache(
            self,
            menu_id: str,
            submenu_id: str
    ) -> None:
        await self.delete_cache_by_mask(
            SUBMENU_URL.format(menu_id=menu_id, submenu_id=submenu_id),
        )
        await self.delete_all_submenu_cache(menu_id=menu_id)

    async def set_all_dishes_cache(
            self,
            menu_id: str,
            submenu_id: str,
            dishes_data: list[Dish]
    ) -> None:
        await self.cacher.set(
            DISHES_URL.format(menu_id=menu_id, submenu_id=submenu_id),
            pickle.dumps(dishes_data),
            ex=EXPIRE,
        )

    async def get_all_dishes_cache(
            self,
            menu_id: str,
            submenu_id: str
    ) -> list[Dish] | None:
        cache = await self.cacher.get(DISHES_URL.format(menu_id=menu_id,
                                                        submenu_id=submenu_id))
        if cache:
            dishes_data = pickle.loads(cache)
            return dishes_data
        return None

    async def set_dish_cache(
            self,
            menu_id: str,
            submenu_id: str,
            dish_data: Dish) -> None:
        await self.cacher.set(
            DISH_URL.format(menu_id=menu_id,
                            submenu_id=submenu_id,
                            dish_id=str(dish_data.id)),
            pickle.dumps(dish_data),
            ex=EXPIRE,
        )

    async def get_dish_cache(
            self,
            menu_id: str,
            submenu_id: str,
            dish_id: str
    ) -> Submenu | None:
        cache = await self.cacher.get(DISH_URL.format(
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_id=dish_id)
        )
        if cache:
            dish_data = pickle.loads(cache)
            return dish_data
        return None

    async def update_dish_cache(
            self,
            menu_id: str,
            submenu_id: str,
            dish_data: Dish
    ) -> None:

        await self.delete_all_dish_cache(
            menu_id=menu_id,
            submenu_id=submenu_id
        )
        await self.set_dish_cache(
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_data=dish_data
        )

    async def delete_all_dish_cache(
            self,
            menu_id: str,
            submenu_id: str
    ) -> None:
        await self.cacher.delete(DISHES_URL.format(
            menu_id=menu_id,
            submenu_id=submenu_id
        )
        )

    async def delete_dish_cache(
            self,
            menu_id: str,
            submenu_id: str,
            dish_id: str
    ) -> None:
        await self.delete_cache_by_mask(
            DISH_URL.format(
                menu_id=menu_id,
                submenu_id=submenu_id,
                dish_id=dish_id
            )
        )
        await self.delete_all_dish_cache(
            menu_id=menu_id,
            submenu_id=submenu_id
        )
