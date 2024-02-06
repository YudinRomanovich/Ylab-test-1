from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm.exc import NoResultFound

from src.config import MENU_INFO_URL, MENU_URL, MENUS_URL
from src.database.schemas import MenuCreate, MenuInfo, MenuRead
from src.menu.service_menu_repo import MenuService

router = APIRouter(
    prefix='/api/v1',
    tags=['Menu']
)


@router.get(
    MENUS_URL,
    response_model=list[MenuRead],
    status_code=200,
    summary='Get all menus'
)
async def get_all_menus(
    background_tasks: BackgroundTasks,
    menu_repo: MenuService = Depends()
) -> list[MenuRead]:
    return await menu_repo.get_menus(background_tasks=background_tasks)


@router.get(
    MENU_URL,
    response_model=MenuRead,
    status_code=200,
    summary='Get a specific menu'
)
async def get_menu(
    menu_id: str,
    background_tasks: BackgroundTasks,
    menu_repo: MenuService = Depends()
) -> MenuRead:
    try:
        return await menu_repo.get_specific_menu(menu_id=menu_id, background_tasks=background_tasks)
    except NoResultFound as e:
        raise HTTPException(
            status_code=404,
            detail=e.args[0],
        )


@router.get(
    MENU_INFO_URL,
    response_model=MenuInfo,
    status_code=200,
    summary='Get specific menu counters'
)
async def get_menu_info(
    menu_id: str,
    background_tasks: BackgroundTasks,
    menu_repo: MenuService = Depends()
):
    try:
        return await menu_repo.get_specific_menu_info(menu_id=menu_id, background_tasks=background_tasks)
    except NoResultFound as e:
        raise HTTPException(
            status_code=404,
            detail=e.args[0],
        )


@router.post(
    MENUS_URL,
    response_model=MenuRead,
    status_code=201,
    summary='Create new menu'
)
async def create_menu(
    menu: MenuCreate,
    background_tasks: BackgroundTasks,
    menu_repo: MenuService = Depends()
) -> MenuRead:
    return await menu_repo.create_menu(menu=menu, background_tasks=background_tasks)


@router.patch(
    MENU_URL,
    response_model=MenuRead,
    status_code=200,
    summary='Update menu'
)
async def update_menu(
    menu_id: str,
    updated_menu: MenuCreate,
    background_tasks: BackgroundTasks,
    menu_repo: MenuService = Depends()
) -> MenuRead:
    try:
        return await menu_repo.update_menu(
            menu_id=menu_id,
            updated_menu=updated_menu,
            background_tasks=background_tasks
        )
    except NoResultFound as e:
        raise HTTPException(
            status_code=404,
            detail=e.args[0],
        )


@router.delete(
    MENU_URL,
    status_code=200,
    summary='Delete menu'
)
async def delete_menu(
    menu_id: str,
    background_tasks: BackgroundTasks,
    menu_repo: MenuService = Depends(),
) -> JSONResponse:
    try:
        await menu_repo.delete_specific_menu(
            menu_id=menu_id,
            background_tasks=background_tasks
        )
        return JSONResponse(
            status_code=200,
            content='menu deleted',
        )
    except NoResultFound as e:
        raise HTTPException(
            status_code=404,
            detail=e.args[0],
        )
