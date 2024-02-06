from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm.exc import NoResultFound

from src.config import SUBMENU_URL, SUBMENUS_URL
from src.database.schemas import SubmenuCreate, SubmenuRead, SubmenuUpdate
from src.submenu.service_submenu_repo import SubmenuService

router = APIRouter(
    prefix='/api/v1',
    tags=['Submenu']
)


@router.get(
    SUBMENU_URL,
    response_model=SubmenuRead,
    status_code=200,
    summary='Get specific submenu',
    responses={404: {'detail': 'submenu not found'}}
)
async def get_submenu(
    menu_id: str,
    submenu_id: str,
    background_tasks: BackgroundTasks,
    repo: SubmenuService = Depends(),
) -> SubmenuRead:
    try:
        return await repo.get_specific_submenu(
            menu_id=menu_id,
            submenu_id=submenu_id,
            background_tasks=background_tasks
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
    summary='Get submenus',
    responses={404: {'detail': 'submenu not found'}}
)
async def get_submenus(
    menu_id: str,
    background_tasks: BackgroundTasks,
    submenu_repo: SubmenuService = Depends()
) -> list[SubmenuRead]:

    return await submenu_repo.get_submenus(menu_id=menu_id, background_tasks=background_tasks)


@router.post(
    SUBMENUS_URL,
    response_model=SubmenuRead,
    status_code=201,
    summary='Create submenu',
    responses={404: {'detail': 'submenu not found'}}
)
async def add_submenu(
    new_submenu: SubmenuCreate,
    menu_id: str,
    background_tasks: BackgroundTasks,
    submenu_repo: SubmenuService = Depends()
) -> SubmenuRead:
    try:
        return await submenu_repo.create_submenu(
            menu_id=menu_id,
            new_submenu=new_submenu,
            background_tasks=background_tasks
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
    summary='Update submenu',
    responses={404: {'detail': 'submenu not found'}}
)
async def update_submenu(
    menu_id: str,
    submenu_id: str,
    updated_submenu: SubmenuUpdate,
    background_tasks: BackgroundTasks,
    submenu_repo: SubmenuService = Depends()
) -> SubmenuRead:
    try:
        return await submenu_repo.update_submenu(
            menu_id=menu_id,
            submenu_id=submenu_id,
            updated_submenu=updated_submenu,
            background_tasks=background_tasks
        )
    except NoResultFound as e:
        raise HTTPException(
            status_code=404,
            detail=e.args[0]
        )


@router.delete(
    SUBMENU_URL,
    status_code=200,
    summary='Delete submenu',
    responses={404: {'detail': 'submenu not found'}}
)
async def delete_submenu(
    menu_id: str,
    submenu_id: str,
    background_tasks: BackgroundTasks,
    submenu_repo: SubmenuService = Depends()
) -> JSONResponse:
    try:
        await submenu_repo.delete_specific_submenu(
            menu_id=menu_id,
            submenu_id=submenu_id,
            background_tasks=background_tasks
        )
        return JSONResponse(
            status_code=200,
            content='submenu deleted',
        )
    except NoResultFound as e:
        raise HTTPException(
            status_code=404,
            detail=e.args[0]
        )
