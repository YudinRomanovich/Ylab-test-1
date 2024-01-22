from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from submenu.utils import create_submenu, get_submenus, update_submenu, delete_submenu


router = APIRouter(
    prefix="/api/v1/menus",
    tags=["Submenu"]
)


@router.get("/{menu_id}/submenus/{submenu_id}")
async def get_submenu(
    submenu_data=Depends(get_submenus)
):
    if not submenu_data:
        raise HTTPException(status_code=404, detail="submenu not found")
    else:
        return submenu_data


@router.get("/{menu_id}/submenus")
async def get_submenu(
    submenu_data=Depends(get_submenus)
):
    return submenu_data


@router.post("/{menu_id}/submenus", status_code=201)
async def add_submenu(
    new_submenu: AsyncSession=Depends(create_submenu)
):
    return new_submenu


@router.patch("/{menu_id}/submenus/{submenu_id}")
async def update_submenu(
    submenu_data=Depends(update_submenu)
):
    return submenu_data


@router.delete("/{menu_id}/submenus/{submenu_id}")
async def delete_submenu(
    deleted_submenu_data=Depends(delete_submenu)
):
    return {
        "detail": f"{deleted_submenu_data}"
    }
