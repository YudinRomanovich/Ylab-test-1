import uuid
from sqlalchemy import Column, ForeignKey, Integer, Numeric, String, Table, UniqueConstraint, UUID
from database.database import metadata


menu = Table(
    "menu",
    metadata,
    Column('id', UUID, primary_key=True, default=uuid.uuid4),
    Column('title', String(255), nullable=False),
    Column('description', String(255), nullable=False),
    Column('submenus_count', Integer, default=0),
    Column('dishes_count', Integer, default=0),
    extend_existing=True
)


dish = Table(
    "dish",
    metadata,
    Column('id', UUID, primary_key=True, default=uuid.uuid4),
    Column('title', String(255), nullable=False),
    Column('description', String(255), nullable=False),
    Column('price', Numeric(10, 2), nullable=False),
    Column('submenu_id', UUID, ForeignKey('submenu.id')),
    UniqueConstraint('title', 'submenu_id')
)


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
