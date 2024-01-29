import uuid

from sqlalchemy import delete, insert, select, update, exists
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends


from database import get_async_session
from menu.models import menu
from submenu.models import submenu
from dish.models import dish
from menu.schemas import MenuCreate, MenuUpdate


async def get_menu_info(menu_id: str = None, session: AsyncSession = Depends(get_async_session)):
    try:
        # Проверка на валидность menu_id
        existing_menu = await session.execute(select(exists().where(menu.c.id == menu_id)))

        if not existing_menu.scalar():
            return None
        query = select(menu.c.title, menu.c.submenus_count, submenu.c.dishes_count).select_from(menu.join(submenu, menu.c.id == submenu.c.menu_id)).where(menu.c.id == menu_id)        

        result = await session.execute(query)
        result = result.all()
        
        menu_data = []

        for item in result:
            menu_data.append({
                "menu title": item[0],
                "submenus": item[1],
                "dishes": item[2]
            })
    except:
        return None

    return menu_data


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
        "submenus_count": item[-1][3],
        "dishes_count": item[-1][3]
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
        "submenus_count": result[3],
        "dishes_count": result[4]
    }
    return menu_data


async def delete_menu(menu_id: str, session: AsyncSession=Depends(get_async_session)):
    # find menu
    query = select(menu).where(menu.c.id == menu_id)
    result = await session.execute(query)
    menu_data = result.all()
    # validation
    if not menu_data == []:
        # find submenu id
        query = select(submenu.c.id).where(submenu.c.menu_id == menu_id)
        result = await session.execute(query)
        submenu_ids = result.all()
        
        # delete dish from submenu
        for item in submenu_ids:
            submenu_id = item[0]
            if isinstance(submenu_id, uuid.UUID):
                stmt = delete(dish).where(dish.c.submenu_id == submenu_id)
                await session.execute(stmt)

        # delete submenu
        for item in submenu_ids:
            submenu_id = item[0]
            if isinstance(submenu_id, uuid.UUID):
                stmt = delete(submenu).where(submenu.c.id == submenu_id)
                await session.execute(stmt)
        
        # delete menu
        stmt = delete(menu).where(menu.c.id == menu_id)
        await session.execute(stmt)
        await session.commit()

        return "menu delete success"
    else:
        return "menu not exist"
