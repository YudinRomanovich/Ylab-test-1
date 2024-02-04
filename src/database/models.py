import uuid

from sqlalchemy import (
    DECIMAL,
    UUID,
    Column,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Table,
    UniqueConstraint,
    func,
    select,
)
from sqlalchemy.orm import column_property, relationship

from database.database import Base, metadata


class Dish(Base):

    __tablename__ = 'dish'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    title = Column(
        String(255),
        nullable=False,
    )
    description = Column(
        String(255),
        nullable=False,
    )
    price = Column(
        DECIMAL(scale=2),
        nullable=False,
    )
    submenu_id = Column(
        UUID(as_uuid=True),
        ForeignKey('submenu.id'),
    )
    submenu = relationship(
        'Submenu',
        back_populates='dishes',
    )

    __table_args__ = (
        UniqueConstraint(
            'title',
            'description',
            name='uq_title_description'
        ),
    )


class Submenu(Base):

    __tablename__ = 'submenu'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    title = Column(
        String(255),
        nullable=False,
    )
    description = Column(
        String(255),
        nullable=False,
    )
    menu_id = Column(
        UUID(as_uuid=True),
        ForeignKey('menu.id'),
    )
    dishes = relationship(
        'Dish',
        back_populates='submenu',
        cascade='all, delete',
    )
    menu = relationship(
        'Menu',
        back_populates='submenus',
    )
    dishes_count = column_property(
        select(func.count(Dish.id)).where(
            Dish.submenu_id == id).correlate_except(Dish).scalar_subquery()
    )


class Menu(Base):

    __tablename__ = 'menu'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    title = Column(
        String(255),
        nullable=False,
    )
    description = Column(
        String(255),
        nullable=False,
    )
    submenus = relationship(
        'Submenu',
        back_populates='menu',
        cascade='all, delete',
    )
    submenus_count = column_property(
        select(func.count(Submenu.id)).where(
            Submenu.menu_id == id).correlate_except(Submenu).scalar_subquery()
    )
    dishes_count = column_property(
        select(func.count(Dish.id)).where(Dish.submenu_id.in_(
            select(Submenu.id).where(Submenu.menu_id == id)
        )).correlate_except(Dish).scalar_subquery()
    )


menu = Table(
    'menu',
    metadata,
    Column('id', UUID, primary_key=True, default=uuid.uuid4),
    Column('title', String(255), nullable=False),
    Column('description', String(255), nullable=False),
    Column('submenus_count', Integer, default=0),
    Column('dishes_count', Integer, default=0),
    extend_existing=True
)


dish = Table(
    'dish',
    metadata,
    Column('id', UUID, primary_key=True, default=uuid.uuid4),
    Column('title', String(255), nullable=False),
    Column('description', String(255), nullable=False),
    Column('price', Numeric(10, 2), nullable=False),
    Column('submenu_id', UUID, ForeignKey('submenu.id')),
    UniqueConstraint('title', 'submenu_id')
)


submenu = Table(
    'submenu',
    metadata,
    Column('id', UUID, primary_key=True, default=uuid.uuid4),
    Column('title', String(255), nullable=False),
    Column('description', String(255), nullable=False),
    Column('menu_id', UUID, ForeignKey('menu.id')),
    UniqueConstraint('title', 'menu_id'),
    Column('dishes_count', Integer, default=0)
)
