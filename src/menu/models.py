import uuid
from sqlalchemy import Column, Integer, String, UUID, Table
from database import metadata


menu = Table(
    "menu",
    metadata,
    Column('id', UUID, primary_key=True, default=uuid.uuid4),
    Column('title', String(255), nullable=False),
    Column('description', String(255), nullable=False),
    Column('submenus_count', Integer, default=0)
)
