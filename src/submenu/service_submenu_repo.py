from fastapi import BackgroundTasks, Depends

from src.database.cache_repo import CacheRepository
from src.database.models import Submenu
from src.database.schemas import SubmenuCreate, SubmenuUpdate
from src.submenu.crud_submenu_repo import SubmenuRepository


class SubmenuService:

    def __init__(
        self,
        crud_repo: SubmenuRepository = Depends(),
        cache_repo: CacheRepository = Depends()
    ) -> None:
        self.crud_repo = crud_repo
        self.cache_repo = cache_repo

    async def get_submenus(
        self,
        menu_id: str,
        background_tasks: BackgroundTasks
    ) -> list[Submenu]:
        cache = await self.cache_repo.get_all_submenus_cache(menu_id=menu_id)
        if cache:
            return cache
        submenu_data = await self.crud_repo.get_all_submenus(menu_id=menu_id)
        background_tasks.add_task(self.cache_repo.set_all_submenus_cache, menu_id, submenu_data)
        return submenu_data

    async def get_specific_submenu(
        self,
        menu_id: str,
        submenu_id: str,
        background_tasks: BackgroundTasks
    ) -> Submenu:
        cache = await self.cache_repo.get_submenu_cache(menu_id=menu_id, submenu_id=submenu_id)
        if cache:
            return cache
        submenu_data = await self.crud_repo.get_specific_submenu(submenu_id=submenu_id)
        background_tasks.add_task(
            self.cache_repo.set_submenu_cache,
            menu_id,
            submenu_data
        )
        return submenu_data

    async def create_submenu(
        self,
        menu_id: str,
        new_submenu: SubmenuCreate,
        background_tasks: BackgroundTasks
    ) -> Submenu:
        submenu_data = await self.crud_repo.create_submenu(menu_id=menu_id, new_submenu=new_submenu)
        background_tasks.add_task(
            self.cache_repo.update_submenu_cache,
            menu_id,
            submenu_data
        )
        return submenu_data

    async def update_submenu(
        self,
        menu_id: str,
        submenu_id: str,
        updated_submenu: SubmenuUpdate,
        background_tasks: BackgroundTasks
    ) -> Submenu:
        submenu_data = await self.crud_repo.update_submenu(
            submenu_id=submenu_id,
            updated_submenu=updated_submenu
        )
        background_tasks.add_task(
            self.cache_repo.update_submenu_cache,
            menu_id,
            submenu_data
        )
        return submenu_data

    async def delete_specific_submenu(
        self,
        menu_id: str,
        submenu_id: str,
        background_tasks: BackgroundTasks
    ) -> None:
        background_tasks.add_task(
            self.cache_repo.delete_submenu_cache,
            menu_id,
            submenu_id
        )
        await self.crud_repo.delete_submenu(submenu_id=submenu_id)
