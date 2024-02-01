from decimal import Decimal
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class MenuCreate(BaseModel):
    model_config = ConfigDict()

    title: str
    description: str


class MenuInfo(BaseModel):
    model_config = ConfigDict()

    title: str
    submenus_count: int
    dishes_count: int


class MenuRead(BaseModel):
    model_config = ConfigDict()

    id: UUID
    title: str
    description: str


class MenuUpdate(BaseModel):
    model_config = ConfigDict()

    title: Optional[str]
    description: Optional[str]


class SubmenuCreate(BaseModel):
    model_config = ConfigDict()

    title: str
    description: str


class SubmenuRead(BaseModel):
    model_config = ConfigDict()
    
    id: UUID
    name: str
    menu_id: int
    

class SubmenuUpdate(BaseModel):
    model_config = ConfigDict()

    title: Optional[str]
    description: Optional[str]


class DishCreate(BaseModel):
    model_config = ConfigDict()

    title: str
    description: str
    price: Decimal


class DishUpdate(BaseModel):
    model_config = ConfigDict()

    title: str
    description: str
    price: Decimal


class DishRead(BaseModel):
    model_config = ConfigDict()

    id: UUID
    title: str
    description: str
    price: Decimal