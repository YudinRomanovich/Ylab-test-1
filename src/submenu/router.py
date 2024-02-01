from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from submenu.utils import create_submenu, get_submenus, update_submenu, delete_submenu
from config import SUBMENU_URL, SUBMENUS_URL


router = APIRouter(
    prefix='/api/v1',
    tags=["Submenu"]
)


@router.get(SUBMENU_URL)
async def get_submenu(
    submenu_data=Depends(get_submenus)
):
    if submenu_data == "submenu not found":
        raise HTTPException(status_code=404, detail="submenu not found")
    else:
        return submenu_data


@router.get(SUBMENUS_URL)
async def get_submenu(
    submenu_data=Depends(get_submenus)
):
    return submenu_data


@router.post(SUBMENUS_URL, status_code=201)
async def add_submenu(
    new_submenu: AsyncSession=Depends(create_submenu)
):
    return new_submenu


@router.patch(SUBMENU_URL)
async def update_submenu(
    submenu_data=Depends(update_submenu)
):
    return submenu_data


@router.delete(SUBMENU_URL)
async def delete_submenu(
    deleted_submenu_data=Depends(delete_submenu)
):
    return {
        "detail": f"{deleted_submenu_data}"
    }
