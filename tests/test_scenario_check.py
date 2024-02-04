import pytest
from typing import AsyncGenerator
from httpx._client import AsyncClient
from http import HTTPStatus

from services import reverse


from src.menu.router import (
    get_all_menus,
    get_menu,
    create_menu,
    delete_menu
)

from src.submenu.router import (
    get_submenu,
    get_submenus,
    add_submenu,
    delete_submenu
)

from src.dish.router import (
    get_dish,
    get_dishes,
    add_dish,
    update_dish,
    delete_dish
)


@pytest.mark.asyncio(scope='session')
async def test_create_menu(ac: AsyncGenerator[AsyncClient, None], menu_post: dict[str, str]):

    response = await ac.post(
        reverse(create_menu),
        json=menu_post,
    )
    
    # check that response status HTTP 201 CREATED
    assert response.status_code == HTTPStatus.CREATED

    assert 'id' in response.json()

@pytest.mark.asyncio(scope='session')
async def test_create_submenu(ac: AsyncGenerator[AsyncClient, None], submenu_post: dict[str, str]):

    menu_data = (await ac.get(reverse(get_all_menus))).json()[0]
    menu_id = menu_data['id']

    response = await ac.post(reverse(add_submenu, menu_id=menu_id), json=submenu_post)    

    # check that response status HTTP 201 CREATED
    assert response.status_code == HTTPStatus.CREATED

    submenu_data = (await ac.get(reverse(get_submenus, menu_id=menu_id))).json()[0]

    # check that 'submenu_id' from environment & response are equal
    assert response.json()["id"] == str(submenu_data["id"])


@pytest.mark.asyncio(scope='session')
async def test_create_dish_first(ac: AsyncGenerator[AsyncClient, None], dish_post: dict[str, str]):

    menu_data = (await ac.get(reverse(get_all_menus))).json()[0]
    menu_id = menu_data['id']
    submenu_data = (await ac.get(reverse(get_submenus, menu_id=menu_id))).json()[0]
    submenu_id = submenu_data['id']

    response = await ac.post(reverse(add_dish, menu_id=menu_id, submenu_id=submenu_id), json=dish_post)

    # check that response status HTTP 201 CREATED
    assert response.status_code == HTTPStatus.CREATED

    dish_data = (await ac.get(reverse(get_dishes, menu_id=menu_id, submenu_id=submenu_id))).json()[0]

    # check that 'dish_id' from environment & response are equal
    assert response.json()["id"] == str(dish_data["id"])


@pytest.mark.asyncio(scope='session')
async def test_create_dish_second(ac: AsyncGenerator[AsyncClient, None], dish_second_post: dict[str, str]):

    menu_data = (await ac.get(reverse(get_all_menus))).json()[0]
    menu_id = menu_data['id']
    submenu_data = (await ac.get(reverse(get_submenus, menu_id=menu_id))).json()[0]
    submenu_id = submenu_data['id']

    response = await ac.post(reverse(add_dish, menu_id=menu_id, submenu_id=submenu_id), json=dish_second_post)

    # check that response status HTTP 201 CREATED
    assert response.status_code == HTTPStatus.CREATED

    dish_data = (await ac.get(reverse(get_dishes, menu_id=menu_id, submenu_id=submenu_id))).json()[0]

    # check that 'dish_id' from environment & response are equal
    assert response.json()["id"] == str(dish_data["id"])



@pytest.mark.asyncio(scope='session')
async def test_get_specific_menu_first(ac: AsyncGenerator[AsyncClient, None]):

    menu_data = (await ac.get(reverse(get_all_menus))).json()[0]
    menu_id = menu_data['id']

    response = await ac.get(
        reverse(get_menu, menu_id=menu_id)
    )

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK

    # check that 'menu_id' from environment & response are equal
    assert response.json()["id"] == str(menu_data["id"])

    # check that 'submenus_count' from environment & response are equal
    assert response.json()["submenus_count"] == menu_data["submenus_count"]

    # check that 'dishes_count' from environment & response are equal
    assert response.json()["dishes_count"] == menu_data["dishes_count"]


@pytest.mark.asyncio(scope='session')
async def test_get_specific_submenu(ac: AsyncGenerator[AsyncClient, None]):

    menu_data = (await ac.get(reverse(get_all_menus))).json()[0]
    menu_id = menu_data['id']
    submenu_data = (await ac.get(reverse(get_submenus, menu_id=menu_id))).json()[0]
    submenu_id = submenu_data['id']

    response = await ac.get(reverse(get_submenu, menu_id=menu_id, submenu_id=submenu_id))

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK

    # check that 'submenu_id' from environment & response are equal
    assert response.json()["id"] == str(submenu_data["id"])

    # check that 'dishes_count' from environment & response are equal
    assert response.json()["dishes_count"] == submenu_data["dishes_count"]


@pytest.mark.asyncio(scope='session')
async def test_delete_submenu(ac: AsyncGenerator[AsyncClient, None], override_get_async_session):

    menu_data = (await ac.get(reverse(get_all_menus))).json()[0]
    menu_id = menu_data['id']
    submenu_data = (await ac.get(reverse(get_submenus, menu_id=menu_id))).json()[0]
    submenu_id = submenu_data['id']

    response = await ac.delete(reverse(delete_submenu, menu_id=menu_id, submenu_id=submenu_id))

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK

    response = await ac.get(reverse(get_dishes, menu_id=menu_id, submenu_id=submenu_id))

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK 

    # check that dish is not exist
    assert response.json() == []


@pytest.mark.asyncio(scope='session')
async def test_get_submenus(ac: AsyncGenerator[AsyncClient, None]):

    menu_data = (await ac.get(reverse(get_all_menus))).json()[0]
    menu_id = menu_data['id']

    submenu_data = (await ac.get(reverse(get_submenus, menu_id=menu_id)))

    # check that response status HTTP 200 OK
    assert submenu_data.status_code == HTTPStatus.OK
    
    # check that response is not empty list
    assert submenu_data.json() == []


@pytest.mark.asyncio(scope='session')
async def test_get_specific_menu(ac: AsyncGenerator[AsyncClient, None]):

    menu_data = (await ac.get(reverse(get_all_menus))).json()[0]
    menu_id = menu_data['id']

    response = await ac.get(
        reverse(get_menu, menu_id=menu_id)
    )

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK

    # check that 'menu_id' from environment & response are equal
    assert response.json()["id"] == str(menu_data["id"])

    # check that 'submenus_count' from environment & response are equal
    assert response.json()["submenus_count"] == menu_data["submenus_count"]

    # check that 'dishes_count' from environment & response are equal
    assert response.json()["dishes_count"] == menu_data["dishes_count"]


@pytest.mark.asyncio(scope='session')
async def test_delete_menu(ac: AsyncGenerator[AsyncClient, None]):
    
    menu_data = (await ac.get(reverse(get_all_menus))).json()[0]
    menu_id = menu_data['id']

    response = await ac.delete(
        reverse(delete_menu, menu_id=menu_id)
    )

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK


@pytest.mark.asyncio(scope='session')
async def test_get_menus(ac: AsyncGenerator[AsyncClient, None]):
    response = await ac.get(
        reverse(get_all_menus)
    )

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK

    # check that response is empty list
    assert response.json() == []
