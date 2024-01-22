from typing import Optional
from pydantic import BaseModel, ConfigDict


class SubmenuCreate(BaseModel):
    model_config = ConfigDict()

    title: str
    description: str


class SubmenuRead(BaseModel):
    model_config = ConfigDict()
    
    id: int
    name: str
    menu_id: int
    

class SubmenuUpdate(BaseModel):
    model_config = ConfigDict()

    title: Optional[str]
    description: Optional[str]
