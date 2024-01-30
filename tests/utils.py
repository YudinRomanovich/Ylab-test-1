from sqlalchemy import select
from src.menu.models import menu


async def get_menu(session, menu_id: str=None):

    if menu_id:
        query = select(menu).where(menu.c.id == menu_id)
        # check that new record added to the database
        response = await session.execute(query)
        result = response.fetchone()
    else:
        query = select(menu)
        response = await session.execute(query)
        result = response.fetchall()


    return result