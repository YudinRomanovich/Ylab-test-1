from database.cache_repo import CacheRepository
from dish.crud_dish_repo import DishRepository
from fastapi import BackgroundTasks, Depends
from database.models import Dish
from database.schemas import DishCreate, DishUpdate


class DishService:

    def __init__(
        self,
        crud_repo: DishRepository = Depends(),
        cache_repo: CacheRepository = Depends()
    ) -> None:
        self.crud_repo = crud_repo
        self.cache_repo = cache_repo

    async def get_dishes(
        self,
        menu_id: str,
        submenu_id: str,
        background_tasks: BackgroundTasks
    ) -> list[Dish]:
        cache = await self.cache_repo.get_all_dishes_cache(menu_id=menu_id, submenu_id=submenu_id)
        if cache:
            return cache
        dish_data = await self.crud_repo.get_all_dishes(submenu_id=submenu_id)
        background_tasks.add_task(self.cache_repo.set_all_dishes_cache, menu_id, submenu_id, dish_data)
        return dish_data
    
    async def get_specific_dish(
        self,
        menu_id: str,
        submenu_id: str,
        dish_id: str,
        background_tasks: BackgroundTasks
    ) -> Dish:
        cache = await self.cache_repo.get_dish_cache(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
        if cache:
            return cache
        dish_data = await self.crud_repo.get_specific_dish(dish_id=dish_id)
        background_tasks.add_task(
            self.cache_repo.set_dish_cache,
            menu_id,
            submenu_id,
            dish_data
        )
        return dish_data

    async def create_dish(
        self,
        menu_id: str,
        submenu_id: str,
        new_dish: DishCreate,
        background_tasks: BackgroundTasks
    ) -> Dish:
        dish_data = await self.crud_repo.create_dish(menu_id=menu_id, submenu_id=submenu_id, dish_data=new_dish)
        background_tasks.add_task(
            self.cache_repo.update_dish_cache,
            menu_id,
            submenu_id,
            dish_data
        )
        return dish_data
    
    async def update_dish(
        self,
        menu_id: str,
        submenu_id: str,
        dish_id: str,
        updated_dish: DishUpdate,
        background_tasks: BackgroundTasks
    ) -> Dish:
        dish_data = await self.crud_repo.update_specific_dish(
            dish_id=dish_id,
            updated_dish=updated_dish
        )
        background_tasks.add_task(
            self.cache_repo.update_dish_cache,
            menu_id,
            submenu_id,
            dish_data
        )
        return dish_data
    
    async def delete_specific_dish(
        self,
        menu_id: str,
        submenu_id: str,
        dish_id: str,
        background_tasks: BackgroundTasks
    ) -> None:
        background_tasks.add_task(
            self.cache_repo.delete_dish_cache,
            menu_id,
            submenu_id,
            dish_id
        )
        await self.crud_repo.delete_specific_dish(dish_id=dish_id)