from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm.exc import NoResultFound
from config import SUBMENU_URL, SUBMENUS_URL
from database.schemas import SubmenuRead, SubmenuCreate, SubmenuUpdate
from submenu.submenu_crud_repo import SubmenuRepository


router = APIRouter(
    prefix='/api/v1',
    tags=["Submenu"]
)


@router.get(
    SUBMENU_URL,
    response_model=SubmenuRead,
    status_code=200,
    summary="Get specific submenu"
)
async def get_submenu(
    menu_id: str,
    submenu_id: str,
    repo: SubmenuRepository = Depends(),
) -> SubmenuRead:
    try:
        return await repo.get_specific_submenu(
            submenu_id=submenu_id
        )
    except NoResultFound as e:
        raise HTTPException(
            status_code=404,
            detail=e.args[0],
        )


@router.get(
    SUBMENUS_URL,
    response_model=list[SubmenuRead],
    status_code=200,
    summary="Get submenus"
)
async def get_submenus(
    menu_id: str,
    submenu_repo: SubmenuRepository = Depends()
) -> list[SubmenuRead]:

    return await submenu_repo.get_all_submenus(menu_id=menu_id)


@router.post(
    SUBMENUS_URL,
    response_model=SubmenuRead,
    status_code=201,
    summary="Create submenu"
)
async def add_submenu(
    new_submenu: SubmenuCreate,
    menu_id: str,
    submenu_repo: SubmenuRepository = Depends()
) -> SubmenuRead:
    try:
        return await submenu_repo.create_submenu(
            menu_id=menu_id,
            new_submenu=new_submenu
        )
    except NoResultFound as e:
        raise HTTPException(
            status_code=404,
            detail=e.args[0]
        )


@router.patch(
    SUBMENU_URL,
    response_model=SubmenuRead,
    status_code=200,
    summary="Update submenu"
)
async def update_submenu(
    menu_id: str,
    submenu_id: str,
    updated_submenu: SubmenuUpdate,
    submenu_repo: SubmenuRepository = Depends()
) -> SubmenuRead:
    try:
        return await submenu_repo.update_submenu(
            submenu_id=submenu_id,
            updated_submenu=updated_submenu
        )
    except NoResultFound as e:
        raise HTTPException(
            status_code=404,
            detail=e.args[0]
        )


@router.delete(
    SUBMENU_URL,
    status_code=200,
    summary="Delete submenu"
)
async def delete_submenu(
    menu_id: str,
    submenu_id: str,
    submenu_repo: SubmenuRepository = Depends()
) -> JSONResponse:
    try:
        await submenu_repo.delete_submenu(submenu_id=submenu_id)
        return JSONResponse(
            status_code=200,
            content='submenu deleted',
        )
    except NoResultFound as e:
        raise HTTPException(
            status_code=404,
            detail=e.args[0]
        )
