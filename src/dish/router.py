from fastapi import APIRouter, Depends, HTTPException
from dish.utils import create_dish, get_dishes, update_dish, delete_dish
from config import DISH_URL, DISHES_URL
from database.schemas import DishRead, DishCreate


router = APIRouter(
    prefix='/api/v1',
    tags=["Dishes"]
)


@router.get(
    DISHES_URL,
    response_model=list[DishRead],
    status_code=200,
    summary="All dishes"
)
async def get_all_dishes(
    dishes_data: DishRead=Depends(get_dishes)
) -> list[DishRead]:
    return dishes_data


@router.get(DISH_URL)
async def get_dish(
    dishes_data: dict=Depends(get_dishes)
):

    if dishes_data == "dish not found":
        raise HTTPException(status_code=404, detail="dish not found")
    else:
        return dishes_data


@router.post(DISHES_URL, status_code=201)
async def add_dish(
    new_dish=Depends(create_dish)
):
    return new_dish


@router.patch(DISH_URL)
async def update_dish(
    updated_dish=Depends(update_dish)
):
    return updated_dish


@router.delete(DISH_URL)
async def delete_dish(
    deleted_dish_data=Depends(delete_dish)
):
        return {
            "detail": f"{deleted_dish_data}"
        }
