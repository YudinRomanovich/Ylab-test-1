from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from menu.crud_menu_repo import MenuRepository
from config import MENU_URL, MENUS_URL, MENU_INFO_URL
from sqlalchemy.orm.exc import NoResultFound
from database.schemas import MenuRead, MenuCreate, MenuInfo


router = APIRouter(
    prefix='/api/v1',
    tags=["Menu"]
)


@router.get(
    MENUS_URL,
    response_model=list[MenuRead],
    status_code=200,
    summary="Get all menus"
)
async def get_all_menus(
    menu_repo: MenuRepository = Depends()
) -> MenuRead:
    return await menu_repo.get_menus()


@router.get(
    MENU_URL,
    response_model=MenuRead,
    status_code=200,
    summary="Get a specific menu"
)
async def get_menu(
    menu_id: str,
    menu_repo: MenuRepository = Depends()
) -> MenuRead:
    try:
        return await menu_repo.get_specific_menu(menu_id=menu_id)
    except NoResultFound as e:
        raise HTTPException(
            status_code=404,
            detail=e.args[0],
        )


@router.get(
    MENU_INFO_URL,
    response_model=MenuInfo,
    status_code=200,
    summary="Get specific menu counters"
)
async def get_menu_info(
    menu_id: str,
    menu_repo: MenuRepository = Depends()
):
    try:
        return await menu_repo.get_specific_menu_info(menu_id=menu_id)
    except NoResultFound as e:
        raise HTTPException(
            status_code=404,
            detail=e.args[0],
        )


@router.post(
    MENUS_URL,
    response_model=MenuRead,
    status_code=201,
    summary="Create new menu"
)
async def add_menu(
    menu: MenuCreate,
    menu_repo: MenuRepository = Depends()
) -> MenuRead:
    return await menu_repo.create_menu(new_menu=menu)


@router.patch(
    MENU_URL,
    response_model=MenuRead,
    status_code=200,
    summary="Update menu"
)
async def update_menu(
    menu_id: str,
    updated_menu: MenuCreate,
    menu_repo: MenuRepository = Depends()
) -> MenuRead:
    try:
        return await menu_repo.update_menu(
            menu_id=menu_id,
            updated_menu=updated_menu
        )
    except NoResultFound as e:
        raise HTTPException(
            status_code=404,
            detail=e.args[0],
        )


@router.delete(
    MENU_URL,
    status_code=200,
    summary="Delete menu"
)
async def delete_menu(
    menu_id: str,
    repo: MenuRepository = Depends(),
) -> JSONResponse:
    try:
        await repo.delete_specific_menu(
            menu_id=menu_id,
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
