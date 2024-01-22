from typing import Optional
from pydantic import BaseModel, ConfigDict


class MenuCreate(BaseModel):
    model_config = ConfigDict()

    title: str
    description: str


class MenuRead(BaseModel):
    model_config = ConfigDict()

    id: int
    title: str
    description: str


class MenuUpdate(BaseModel):
    model_config = ConfigDict()

    title: Optional[str]
    description: Optional[str]
