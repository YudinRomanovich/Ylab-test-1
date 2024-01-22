from decimal import Decimal
from pydantic import BaseModel, ConfigDict


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

    id: int
    name: str
    price: Decimal
    submenu_id: int
