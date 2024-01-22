from fastapi import APIRouter, Depends, HTTPException
from dish.utils import create_dish, get_dishes, update_dish, delete_dish


router = APIRouter(
    prefix="/api/v1/menus",
    tags=["Dish"]
)


@router.get("/{menu_id}/submenus/{submenu_id}/dishes")
async def get_all_dishes(
    dishes_data=Depends(get_dishes)
):
    return dishes_data


@router.get("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
async def get_dish(
    dishes_data: dict=Depends(get_dishes)
):

    if dishes_data == None:
        raise HTTPException(status_code=404, detail="dish not found")
    else:
        return dishes_data


@router.post("/{menu_id}/submenus/{submenu_id}/dishes", status_code=201)
async def add_dish(
    new_dish=Depends(create_dish)
):
    return new_dish


@router.patch("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
async def update_dish(
    updated_dish=Depends(update_dish)
):
    return updated_dish


@router.delete("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
async def delete_dish(
    deleted_dish_data=Depends(delete_dish)
):
        return {
            "detail": f"{deleted_dish_data}"
        }
