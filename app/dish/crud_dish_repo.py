from database.database_main import get_async_session
from database.models import Dish
from database.schemas import DishCreate, DishUpdate
from database.services import check_objects
from fastapi import Depends
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound
from submenu.crud_submenu_repo import SubmenuRepository


class DishRepository:

    def __init__(
            self,
            session: AsyncSession = Depends(get_async_session),
            submenu_repo: SubmenuRepository = Depends()
    ) -> None:
        self.session = session
        self.submenu_repo = submenu_repo
        self.model = Dish

    async def create_dish(
            self,
            dish_data: DishCreate,
            menu_id: str,
            submenu_id: str
    ) -> Dish:
        try:
            await check_objects(
                session=self.session,
                menu_id=menu_id,
                submenu_id=submenu_id,
            )
        except NoResultFound as error:
            raise NoResultFound(error.args[0])

        stmt = insert(self.model).values(
            **dish_data.model_dump(),
            submenu_id=submenu_id
        )
        await self.session.execute(stmt)
        await self.session.commit()

        return await self.get_specific_dish(self.model.id)

    async def get_specific_dish(
            self,
            dish_id: str
    ) -> Dish:
        dish = (await self.session.execute(
            select(self.model).where(self.model.id == dish_id)
        )).scalar()
        if not dish:
            raise NoResultFound('dish not found')
        return dish

    async def get_all_dishes(
            self,
            submenu_id: str
    ) -> list[Dish]:
        try:
            await check_objects(session=self.session, submenu_id=submenu_id)
        except NoResultFound:
            return []
        return ((await self.session.execute(
            select(self.model).where(self.model.submenu_id == submenu_id)
        )).scalars().all())

    async def update_specific_dish(
            self,
            dish_id: str,
            updated_dish: DishUpdate
    ) -> Dish:
        dish_data = await self.get_specific_dish(dish_id=dish_id)
        if not dish_data:
            raise NoResultFound('dish not found')

        dish_data.title = updated_dish.title
        dish_data.description = updated_dish.description
        dish_data.price = updated_dish.price
        await self.session.merge(dish_data)
        await self.session.commit()
        await self.session.refresh(dish_data)
        return dish_data

    async def delete_specific_dish(
            self,
            dish_id: str
    ) -> None:
        dish_data = await self.get_specific_dish(dish_id=dish_id)

        if not dish_data:
            raise NoResultFound('menu not found')
        else:
            await self.session.delete(dish_data)
            await self.session.commit()
