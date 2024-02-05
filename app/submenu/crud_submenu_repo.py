from fastapi import Depends
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound
from src.database.database_main import get_async_session
from src.database.models import Submenu
from src.database.schemas import SubmenuCreate, SubmenuUpdate
from src.database.services import check_objects
from src.menu.crud_menu_repo import MenuRepository


class SubmenuRepository:

    def __init__(
        self,
        menu_repo: MenuRepository = Depends(),
        session: AsyncSession = Depends(get_async_session)
    ) -> None:
        self.session = session
        self.menu_repo = menu_repo
        self.model = Submenu

    async def get_specific_submenu(self, submenu_id: str) -> Submenu:

        submenu_data = (await self.session.execute(
            select(self.model).where(self.model.id == submenu_id)
        )).scalar()

        if not submenu_data:
            raise NoResultFound('submenu not found')
        return submenu_data

    async def get_all_submenus(self, menu_id: str) -> list[Submenu]:
        try:
            await check_objects(session=self.session, menu_id=menu_id)
        except NoResultFound:
            return []
        else:
            return ((await self.session.execute(
                select(self.model).where(self.model.menu_id == menu_id),
            )).scalars().all())

    async def create_submenu(
            self,
            menu_id: str,
            new_submenu: SubmenuCreate
    ) -> Submenu:

        try:
            await check_objects(
                session=self.session,
                menu_id=menu_id,
            )
        except NoResultFound as error:
            raise NoResultFound(error.args[0])

        stmt = insert(Submenu).values(
            **new_submenu.model_dump(),
            menu_id=menu_id
        )
        await self.session.execute(stmt)
        await self.session.commit()

        # fetch the newly created object to return it
        return await self.get_specific_submenu(self.model.id)

    async def update_submenu(
            self,
            submenu_id: str,
            updated_submenu: SubmenuUpdate
    ) -> Submenu:

        submenu_data = await self.get_specific_submenu(submenu_id=submenu_id)

        if not submenu_data:
            raise NoResultFound('menu not found')
        else:
            submenu_data.title = updated_submenu.title
            submenu_data.description = updated_submenu.description
            await self.session.merge(submenu_data)
            await self.session.commit()
            await self.session.refresh(submenu_data)
            return submenu_data

    async def delete_submenu(self, submenu_id: str) -> None:

        submenu_data = await self.get_specific_submenu(submenu_id=submenu_id)

        if not submenu_data:
            raise NoResultFound('menu not found')
        else:
            await self.session.delete(submenu_data)
            await self.session.commit()
