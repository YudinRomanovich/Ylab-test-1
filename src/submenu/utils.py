from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from src.database.database import get_async_session
from src.database.models import submenu
from submenu.schemas import SubmenuCreate, SubmenuUpdate
from src.database.models import menu
from src.database.models import dish


async def get_submenus(menu_id: str=None, submenu_id: str=None, submenu_data=None, session: AsyncSession=Depends(get_async_session)):
    
    if menu_id and submenu_id:
        """return specific submenu or None"""
        query = select(submenu).where(submenu.c.menu_id == menu_id)
        result = await session.execute(query)
        ans = result.all()

        if ans == []:
            submenu_data = "submenu not found"
        else:
            query = select(submenu).where(submenu_id == submenu.c.id)
            result = await session.execute(query)
            for item in result.all():
                submenu_data = {
                    "id": item[0],
                    "title": item[1],
                    "description": item[2],
                    "dishes_count": item[4]
                }
    else:
        query = select(submenu).where(menu_id == submenu.c.menu_id)
        result = await session.execute(query)
        submenu_data = []
        for item in result.all():
            submenu_data.append({
                "id": item[0],
                "title": item[1],
                "description": item[2],
                "dishes_count": item[4]
            })

    return submenu_data


async def create_submenu(menu_id: str, new_submenu: SubmenuCreate, session: AsyncSession=Depends(get_async_session)):
    # проверить существует ли такое меню если нет то создаем подменю без указания подменю
    query = select(menu).where(menu_id == menu.c.id)
    result = await session.execute(query)
    
    if not result.all() == []:
        stmt = insert(submenu).values(**new_submenu.model_dump(), menu_id=menu_id)
        await session.execute(stmt)
        await session.commit()

        stmt = update(menu).where(menu_id == menu.c.id).values(submenus_count=menu.c.submenus_count + 1)
        await session.execute(stmt)
        await session.commit()
        
    else:
        stmt = insert(submenu).values(**new_submenu.model_dump())
        await session.execute(stmt)
        await session.commit()



    query = select(submenu)
    result = await session.execute(query)
    items = result.all()
    
    submenu_data = {
        "id": items[-1][0],
        "title": items[-1][1],
        "description": items[-1][2],
        "dishes_count": items[-1][4]
    }
    return submenu_data


async def update_submenu(submenu_id: str, new_updated_submenu: SubmenuUpdate, session: AsyncSession=Depends(get_async_session)):
    
    stmt = update(submenu).where(submenu_id == submenu.c.id).values(**new_updated_submenu.model_dump())
    await session.execute(stmt)
    await session.commit()

    query = select(submenu).where(submenu_id == submenu.c.id)
    result = await session.execute(query)
    result = result.all()[-1]
    submenu_data = {
        "id": result[0],
        "title": result[1],
        "description": result[2],
        "dishes_count": result[4]
    }
    return submenu_data


async def delete_submenu(submenu_id: str, session: AsyncSession=Depends(get_async_session)):
    # search menu_id
    query = select(submenu).where(submenu_id == submenu.c.id)
    result = await session.execute(query)
    menu_id = result.all()[0][-2]

    # update submenu counter in menu
    stmt = update(menu).where(menu_id == menu.c.id).values(submenus_count=menu.c.submenus_count - 1)
    await session.execute(stmt)
    await session.commit()

    # delete dishes from current submenu
    stmt = delete(dish).where(dish.c.submenu_id == submenu_id)
    await session.execute(stmt)
    await session.commit()

    # delete submenu
    stmt = delete(submenu).where(submenu_id == submenu.c.id)
    await session.execute(stmt)
    await session.commit()

    return "deleted submenu success"
