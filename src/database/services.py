from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound

from database.models import Dish, Menu, Submenu


async def check_objects(
    session: AsyncSession,
    menu_id: str | None = None,
    submenu_id: str | None = None,
    dish_id: str | None = None,
) -> None:

    if menu_id:
        query = select(exists().where(Menu.id == menu_id))
        exists_menu = await session.scalar(query)
        if not exists_menu:
            raise NoResultFound('menu not found')

    if submenu_id:
        query = select(exists().where(Submenu.id == submenu_id))
        exists_submenu = await session.scalar(query)
        if not exists_submenu:
            raise NoResultFound('submenu not found')

    if dish_id:
        query = select(exists().where(Dish.id == dish_id))
        exists_submenu = await session.scalar(query)
        if not exists_submenu:
            raise NoResultFound('dish not found')
