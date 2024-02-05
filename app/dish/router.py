from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm.exc import NoResultFound
from src.config import DISH_URL, DISHES_URL
from src.database.schemas import DishCreate, DishRead, DishUpdate

from .service_dish_repo import DishService

router = APIRouter(
    prefix='/api/v1',
    tags=['Dishes']
)


@router.get(
    DISHES_URL,
    response_model=list[DishRead],
    status_code=200,
    summary='All dishes'
)
async def get_dishes(
    menu_id: str,
    submenu_id: str,
    background_tasks: BackgroundTasks,
    dish_repo: DishService = Depends()
) -> list[DishRead]:

    return await dish_repo.get_dishes(
        menu_id=menu_id,
        submenu_id=submenu_id,
        background_tasks=background_tasks
    )


@router.get(
    DISH_URL,
    response_model=DishRead,
    status_code=200,
    summary='Get specific dish'
)
async def get_dish(
    menu_id: str,
    submenu_id: str,
    dish_id: str,
    background_tasks: BackgroundTasks,
    dish_repo: DishService = Depends()
) -> DishRead:

    try:
        return await dish_repo.get_specific_dish(
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_id=dish_id,
            background_tasks=background_tasks
        )
    except NoResultFound as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@router.post(
    DISHES_URL,
    status_code=201,
    response_model=DishRead,
    summary='Add new dish'
)
async def add_dish(
    menu_id: str,
    submenu_id: str,
    dish_data: DishCreate,
    background_tasks: BackgroundTasks,
    dish_repo: DishService = Depends()
) -> DishRead:
    try:
        return await dish_repo.create_dish(
            menu_id=menu_id,
            submenu_id=submenu_id,
            new_dish=dish_data,
            background_tasks=background_tasks
        )
    except NoResultFound as e:
        raise HTTPException(
            status_code=404,
            detail=e.args[0]
        )


@router.patch(
    DISH_URL,
    status_code=200,
    response_model=DishRead,
    summary='Update existing dish',
)
async def update_dish(
    menu_id: str,
    submenu_id: str,
    dish_id: str,
    updated_dish: DishUpdate,
    background_tasks: BackgroundTasks,
    dish_repo: DishService = Depends()
) -> DishRead:
    try:
        return await dish_repo.update_dish(
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_id=dish_id,
            updated_dish=updated_dish,
            background_tasks=background_tasks
        )
    except NoResultFound as e:
        raise HTTPException(
            status_code=404,
            detail=e.args[0]
        )


@router.delete(
    DISH_URL,
    response_model=DishRead,
    status_code=200,
    summary='Delete a specific dish',
)
async def delete_dish(
    menu_id: str,
    submenu_id: str,
    dish_id: str,
    background_tasks: BackgroundTasks,
    dish_repo: DishService = Depends()
) -> JSONResponse:
    try:
        await dish_repo.delete_specific_dish(
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_id=dish_id,
            background_tasks=background_tasks
        )
        return JSONResponse(
            status_code=200,
            content='dish deleted',
        )
    except NoResultFound as e:
        raise HTTPException(
            status_code=404,
            detail=e.args[0],
        )
