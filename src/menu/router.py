from fastapi import APIRouter, Depends, HTTPException
from menu.utils import get_menus, get_menu_info, create_menu, update_menu, delete_menu
from config import MENU_URL, MENUS_URL, MENU_INFO_URL


router = APIRouter(
    prefix='/api/v1',
    tags=["Menu"]
)


@router.get(MENUS_URL)
async def get_all_menus(
    menu_data: dict=Depends(get_menus)
):
    return menu_data


@router.get(MENU_URL)
async def get_menu(
    menu_data: dict=Depends(get_menus)
):
    if menu_data == "menu not found":
        raise HTTPException(status_code=404, detail="menu not found")
    else:
        return menu_data


@router.get(MENU_INFO_URL)
async def get_menu_info(
    menu_data: dict=Depends(get_menu_info)
):
    if not menu_data:
        raise HTTPException(status_code=404, detail="menu not exist")
    else:
        return menu_data


@router.post(MENUS_URL, status_code=201)
async def add_menu(
    new_menu=Depends(create_menu)
):
    return new_menu


@router.patch(MENU_URL)
async def update_menu(
    updated_menu=Depends(update_menu)
):
    return updated_menu


@router.delete(MENU_URL)
async def delete_menu(
    deleted_menu_data=Depends(delete_menu)
):
    return {
        "detail": f"{deleted_menu_data}"
    }
