import uuid
from sqlalchemy import Column, ForeignKey, Integer, String, Table, UniqueConstraint, UUID
from database import metadata


submenu = Table(
    "submenu",
    metadata,
    Column('id', UUID, primary_key=True, default=uuid.uuid4),
    Column('title', String(255), nullable=False),
    Column('description', String(255), nullable=False),
    Column('menu_id', UUID, ForeignKey('menu.id')),
    UniqueConstraint('title', 'menu_id'),
    Column('dishes_count', Integer, default=0)
)
