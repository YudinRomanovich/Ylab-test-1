import uuid
from sqlalchemy import Column, ForeignKey, Integer, Numeric, String, Table, UniqueConstraint, UUID
from database import metadata


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
