from fastapi import BackgroundTasks, Depends

from src.database.cache_repo import CacheRepository
from src.database.models import Menu
from src.database.schemas import MenuCreate
from src.menu.crud_menu_repo import MenuRepository


class MenuService:

    def __init__(
        self,
        crud_repo: MenuRepository = Depends(),
        cache_repo: CacheRepository = Depends(),
    ) -> None:
        self.crud_repo = crud_repo
        self.cache_repo = cache_repo

    async def get_menus(
        self,
        background_tasks: BackgroundTasks,
    ) -> list[Menu]:
        cache = await self.cache_repo.get_all_menus_cache()
        if cache:
            return cache
        menu_data = await self.crud_repo.get_menus()
        background_tasks.add_task(self.cache_repo.set_all_menus_cache, menu_data)
        return menu_data

    async def get_specific_menu(
        self,
        menu_id: str,
        background_tasks: BackgroundTasks,
    ) -> Menu:
        cache = await self.cache_repo.get_menu_cache(menu_id=menu_id)
        if cache:
            return cache
        menu_data = await self.crud_repo.get_specific_menu(menu_id=menu_id)
        background_tasks.add_task(
            self.cache_repo.set_menu_cache,
            menu_data,
        )
        return menu_data

    async def get_specific_menu_info(self, menu_id: str, background_tasks: BackgroundTasks) -> Menu:
        cache = await self.cache_repo.get_specific_menu_info_cache(menu_id=menu_id)
        if cache:
            return cache
        menu_data = await self.crud_repo.get_specific_menu_info(menu_id=menu_id)
        background_tasks.add_task(
            self.cache_repo.set_specific_menu_info_cache,
            menu_data
        )
        return menu_data

    async def create_menu(
        self,
        menu: MenuCreate,
        background_tasks: BackgroundTasks,
    ) -> Menu:
        menu_data = await self.crud_repo.create_menu(new_menu=menu)
        background_tasks.add_task(
            self.cache_repo.create_update_menu_cache,
            menu_data
        )
        return menu_data

    async def update_menu(
        self,
        menu_id: str,
        updated_menu: MenuCreate,
        background_tasks: BackgroundTasks,
    ) -> Menu:
        menu_data = await self.crud_repo.update_menu(
            menu_id=menu_id,
            updated_menu=updated_menu,
        )
        background_tasks.add_task(
            self.cache_repo.create_update_menu_cache,
            menu_data,
        )
        return menu_data

    async def delete_specific_menu(
        self,
        menu_id: str,
        background_tasks: BackgroundTasks,
    ) -> None:
        background_tasks.add_task(
            self.cache_repo.delete_menu_cache,
            menu_id,
        )
        await self.crud_repo.delete_specific_menu(menu_id=menu_id)
