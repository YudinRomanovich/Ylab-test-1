from sqlalchemy import delete, insert, select, update, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from database import get_async_session
from menu.models import menu
from submenu.models import submenu
from menu.schemas import MenuCreate, MenuUpdate


async def get_menus(menu_id: str=None, session: AsyncSession=Depends(get_async_session)):

    if not menu_id:
        """return all menu"""
        query = select(menu)
        result = await session.execute(query)
        menu_data = [
            {
                "id": item[0],
                "title": item[1],
                "description": item[2],
                "submenus_count": item[3]
            }
            for item in result.all()
        ]     
    else:
        
        """return specific menu or None"""
        query = select(menu).where(menu_id == menu.c.id)
        result = await session.execute(query)
        ans = result.all()
        
        if ans == []:
            menu_data = None
        else:
            query = select(submenu).where(submenu.c.menu_id == menu_id)
            result = await session.execute(query)
            submenu_data = result.all()
            dishes_count = sum(item[4] for item in submenu_data)
            for item in ans:
                menu_data = {
                    "id": str(item[0]),
                    "title": item[1],
                    "description": item[2],
                    "submenus_count": item[3],
                    "dishes_count": dishes_count
                }
    return menu_data


async def create_menu(new_menu: MenuCreate, session: AsyncSession=Depends(get_async_session)):
    
    stmt = insert(menu).values(**new_menu.model_dump())
    await session.execute(stmt)
    await session.commit()
    query = select(menu)
    result = await session.execute(query)
    item = result.all()
    
    """returned last created menu"""
    menu_data = {
        "id": item[-1][0],
        "title": item[-1][1],
        "description": item[-1][2],
        "submenus_count": item[-1][3]
    }
    
    return menu_data


async def update_menu(menu_id: str, new_updated_menu: MenuUpdate, session: AsyncSession=Depends(get_async_session)):

    stmt = update(menu).where(menu_id == menu.c.id).values(**new_updated_menu.model_dump())
    await session.execute(stmt)
    await session.commit()
    query = select(menu).where(menu_id == menu.c.id)
    result = await session.execute(query)
    result = result.all()[-1]
    menu_data = {
        "id": result[0],
        "title": result[1],
        "description": result[2],
        "submenus_count": result[3]
    }
    return menu_data


async def delete_menu(menu_id: str, session: AsyncSession=Depends(get_async_session)):
    
    query = select(menu).where(menu.c.id == menu_id)
    result = await session.execute(query)
    menu_data = result.all()

    if not menu_data == []:
        stmt = delete(menu).where(menu_id == menu.c.id)
        await session.execute(stmt)
        await session.commit()
        return "menu deleted success"
    else:
        return "menu not exist"
