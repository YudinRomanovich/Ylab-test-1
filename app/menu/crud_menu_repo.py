from database.database_main import get_async_session
from database.models import Menu
from database.schemas import MenuCreate
from fastapi import Depends
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound


class MenuRepository:

    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session
        self.model = Menu

    async def get_specific_menu(self, menu_id: str) -> Menu:

        menu_data = (await self.session.execute(
            select(self.model).where(self.model.id == menu_id)
        )).scalar()

        if not menu_data:
            raise NoResultFound('menu not found')
        return menu_data

    async def get_menus(self) -> list[Menu]:
        return (await self.session.execute(
            select(self.model)
        )).scalars().fetchall()

    async def create_menu(self, new_menu: MenuCreate) -> Menu:

        stmt = insert(Menu).values(**new_menu.model_dump())
        await self.session.execute(stmt)
        await self.session.commit()

        # fetch the newly created object to return it
        return await self.get_specific_menu(self.model.id)

    async def update_menu(
            self, menu_id: str,
            updated_menu: MenuCreate
    ) -> Menu:

        menu_data = await self.get_specific_menu(menu_id=menu_id)

        if not menu_data:
            raise NoResultFound('menu not found')
        else:
            menu_data.title = updated_menu.title
            menu_data.description = updated_menu.description
            await self.session.merge(menu_data)
            await self.session.commit()
            await self.session.refresh(menu_data)
            return menu_data

    async def delete_specific_menu(self, menu_id: str) -> None:

        menu_data = await self.get_specific_menu(menu_id=menu_id)

        if not menu_data:
            raise NoResultFound('menu not found')
        else:
            await self.session.delete(menu_data)
            await self.session.commit()

    async def get_specific_menu_info(self, menu_id: str):

        menu_data = await self.get_specific_menu(menu_id=menu_id)

        if not menu_data:
            raise NoResultFound('menu not found')

        query = select(
            Menu.title,
            Menu.submenus_count,
            Menu.dishes_count
        ).where(Menu.id == menu_id)

        result = await self.session.execute(query)
        menu_info = result.fetchone()

        # Преобразование результата в словарь
        menu_info_dict = dict(zip(result.keys(), menu_info))

        return menu_info_dict
