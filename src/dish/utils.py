from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from database import get_async_session
from dish.models import dish
from submenu.models import submenu
from dish.schemas import DishCreate, DishUpdate


async def get_dishes(submenu_id: str=None, dish_id: str=None, session: AsyncSession=Depends(get_async_session)):
    if not dish_id:
        quary = select(dish).where(submenu_id == dish.c.submenu_id)
        result = await session.execute(quary)
        dish_data = []
        for item in result.all():
            dish_data.append({
                "id": item[0],
                "title": item[1],
                "description": item[2],
                "price": str(item[3])
            })

    else:

        quary = select(dish).where(dish_id == dish.c.id)
        result = await session.execute(quary)
        result = result.all()
        if result == []:
            dish_data = "dish not found"
        else:
            for item in result:
                dish_data = {
                    "id": item[0],
                    "title": item[1],
                    "description": item[2],
                    "price": str(item[3])            
                }

    return dish_data

async def create_dish(submenu_id: str, new_dish: DishCreate, session: AsyncSession=Depends(get_async_session)):
    # проверить существует ли подменю
    query = select(submenu).where(submenu.c.id == submenu_id)
    result = await session.execute(query)
    
    if not result.all() == []:

        stmt = insert(dish).values(**new_dish.model_dump(), submenu_id=submenu_id)
        await session.execute(stmt)
        await session.commit()

        stmt = update(submenu).where(submenu_id == submenu.c.id).values(dishes_count=submenu.c.dishes_count + 1)
        await session.execute(stmt)
        await session.commit()

    else:

        stmt = insert(dish).values(**new_dish.model_dump())
        await session.execute(stmt)
        await session.commit()


    quary = select(dish)
    result = await session.execute(quary)
    items = result.all()
    
    dish_data = {
        "id": items[-1][0],
        "title": items[-1][1],
        "description": items[-1][2],
        "price": str(items[-1][3])
    }
    
    return dish_data

async def update_dish(dish_id: str, updated_dish: DishUpdate, session: AsyncSession=Depends(get_async_session)):
    stmt = update(dish).where(dish_id == dish.c.id).values(**updated_dish.model_dump())
    await session.execute(stmt)
    await session.commit()

    quary = select(dish).where(dish_id == dish.c.id)
    result = await session.execute(quary)
    result = result.all()[-1]
    dish_data = {
        "id": result[0],
        "title": result[1],
        "description": result[2],
        "price": str(result[3])
    }
    return dish_data


async def delete_dish(dish_id: str, session: AsyncSession=Depends(get_async_session)):

    query = select(dish).where(dish_id == dish.c.id)
    result = await session.execute(query)
    submenu_id = result.all()[0][-1]

    stmt = update(submenu).where(submenu_id == submenu.c.id).values(dishes_count=submenu.c.dishes_count - 1)
    await session.execute(stmt)
    await session.commit()

    stmt = delete(dish).where(dish_id == dish.c.id)
    await session.execute(stmt)
    await session.commit()
