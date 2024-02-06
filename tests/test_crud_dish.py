from http import HTTPStatus

import pytest
from httpx._client import AsyncClient

from src.dish.router import add_dish, delete_dish, get_dish, get_dishes, update_dish
from src.menu.router import create_menu, delete_menu, get_all_menus
from src.submenu.router import add_submenu, delete_submenu, get_submenus

from .services import reverse


async def test_create_menu(ac: AsyncClient, menu_post: dict[str, str]) -> None:

    response = await ac.post(
        reverse(create_menu),
        json=menu_post,
    )

    # check that response status HTTP 201 CREATED
    assert response.status_code == HTTPStatus.CREATED

    assert 'id' in response.json()


async def test_create_submenu(ac: AsyncClient, submenu_post: dict[str, str]):

    menu_data = (await ac.get(reverse(get_all_menus))).json()[0]
    menu_id = menu_data['id']

    response = await ac.post(reverse(add_submenu, menu_id=menu_id), json=submenu_post)

    # check that response status HTTP 201 CREATED
    assert response.status_code == HTTPStatus.CREATED

    submenu_data = (await ac.get(reverse(get_submenus, menu_id=menu_id))).json()[0]

    # check that 'submenu_id' from environment & response are equal
    assert response.json()['id'] == str(submenu_data['id'])


@pytest.mark.asyncio(scope='session')
async def test_get_dishes_first(ac: AsyncClient):

    menu_data = (await ac.get(reverse(get_all_menus))).json()[0]
    menu_id = menu_data['id']
    submenu_data = (await ac.get(reverse(get_submenus, menu_id=menu_id))).json()[0]
    submenu_id = submenu_data['id']

    response = await ac.get(reverse(get_dishes, menu_id=menu_id, submenu_id=submenu_id))

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK

    # check that response is empty list
    assert response.json() == []


@pytest.mark.asyncio(scope='session')
async def test_create_dish(ac: AsyncClient, dish_post: dict[str, str]):

    menu_data = (await ac.get(reverse(get_all_menus))).json()[0]
    menu_id = menu_data['id']
    submenu_data = (await ac.get(reverse(get_submenus, menu_id=menu_id))).json()[0]
    submenu_id = submenu_data['id']

    response = await ac.post(reverse(add_dish, menu_id=menu_id, submenu_id=submenu_id), json=dish_post)

    # check that response status HTTP 201 CREATED
    assert response.status_code == HTTPStatus.CREATED

    dish_data = (await ac.get(reverse(get_dishes, menu_id=menu_id, submenu_id=submenu_id))).json()[0]

    # check that 'dish_id' from environment & response are equal
    assert response.json()['id'] == str(dish_data['id'])

    # check that 'dish_title' from environment & response are equal
    assert response.json()['title'] == dish_data['title']

    # check that 'dish_description' from environment & response are equal
    assert response.json()['description'] == dish_data['description']

    # check that 'dish_price' from environment & response are equal
    assert response.json()['price'] == dish_data['price']


@pytest.mark.asyncio(scope='session')
async def test_get_dishes_second(ac: AsyncClient):

    menu_data = (await ac.get(reverse(get_all_menus))).json()[0]
    menu_id = menu_data['id']
    submenu_data = (await ac.get(reverse(get_submenus, menu_id=menu_id))).json()[0]
    submenu_id = submenu_data['id']

    response = await ac.get(reverse(get_dishes, menu_id=menu_id, submenu_id=submenu_id))

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK

    # check that response is empty list
    assert not response.json() == []


@pytest.mark.asyncio(scope='session')
async def test_get_specific_dish_first(ac: AsyncClient):

    menu_data = (await ac.get(reverse(get_all_menus))).json()[0]
    menu_id = menu_data['id']
    submenu_data = (await ac.get(reverse(get_submenus, menu_id=menu_id))).json()[0]
    submenu_id = submenu_data['id']
    dish_data = (await ac.get(reverse(get_dishes, menu_id=menu_id, submenu_id=submenu_id))).json()[0]

    response = await ac.get(reverse(get_dish, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_data['id']))

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK

    # check that 'dish_id' from environment & response are equal
    assert response.json()['id'] == str(dish_data['id'])

    # check that 'dish_title' from environment & response are equal
    assert response.json()['title'] == dish_data['title']

    # check that 'dish_description' from environment & response are equal
    assert response.json()['description'] == dish_data['description']

    # check that 'dish_price' from environment & response are equal
    assert response.json()['price'] == dish_data['price']


@pytest.mark.asyncio(scope='session')
async def test_update_dish(ac: AsyncClient, dish_patch: dict[str, str]):

    menu_data = (await ac.get(reverse(get_all_menus))).json()[0]
    menu_id = menu_data['id']
    submenu_data = (await ac.get(reverse(get_submenus, menu_id=menu_id))).json()[0]
    submenu_id = submenu_data['id']
    dish_data = (await ac.get(reverse(get_dishes, menu_id=menu_id, submenu_id=submenu_id))).json()[0]

    response = await ac.patch(reverse(update_dish, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_data['id']), json=dish_patch)

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK

    # check that 'dish_title' from environment & response are not equal
    assert not response.json()['title'] == dish_data['title']

    # check that 'dish_description' from environment & response are not equal
    assert not response.json()['description'] == dish_data['description']

    # check that 'dish_price' from environment & response are not equal
    assert not response.json()['price'] == dish_data['price']

    dish_data = (await ac.get(reverse(get_dish, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_data['id']))).json()

    # check that 'dish_title' from environment & response are equal
    assert response.json()['title'] == dish_data['title']

    # check that 'dish_description' from environment & response are equal
    assert response.json()['description'] == dish_data['description']

    # check that 'dish_price' from environment & response are equal
    assert response.json()['price'] == dish_data['price']


@pytest.mark.asyncio(scope='session')
async def test_get_specific_dish_second(ac: AsyncClient):

    menu_data = (await ac.get(reverse(get_all_menus))).json()[0]
    menu_id = menu_data['id']
    submenu_data = (await ac.get(reverse(get_submenus, menu_id=menu_id))).json()[0]
    submenu_id = submenu_data['id']
    dish_data = (await ac.get(reverse(get_dishes, menu_id=menu_id, submenu_id=submenu_id))).json()[0]

    response = await ac.get(reverse(get_dish, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_data['id']))

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK

    # check that 'dish_id' from environment & response are equal
    assert response.json()['id'] == str(dish_data['id'])

    # check that 'dish_title' from environment & response are equal
    assert response.json()['title'] == dish_data['title']

    # check that 'dish_description' from environment & response are equal
    assert response.json()['description'] == dish_data['description']

    # check that 'dish_price' from environment & response are equal
    assert response.json()['price'] == dish_data['price']


@pytest.mark.asyncio(scope='session')
async def test_delete_dish(ac: AsyncClient):

    menu_data = (await ac.get(reverse(get_all_menus))).json()[0]
    menu_id = menu_data['id']
    submenu_data = (await ac.get(reverse(get_submenus, menu_id=menu_id))).json()[0]
    submenu_id = submenu_data['id']
    dish_data = (await ac.get(reverse(get_dishes, menu_id=menu_id, submenu_id=submenu_id))).json()[0]
    dish_id = dish_data['id']

    response = await ac.delete(reverse(delete_dish, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id))

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK

    response = await ac.get(reverse(get_dish, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id))

    # check that response status HTTP 404 NOT FOUND
    assert response.status_code == HTTPStatus.NOT_FOUND

    # check that 'dish_id' is not exist
    assert response.json()['detail'] == 'dish not found'


@pytest.mark.asyncio(scope='session')
async def test_get_dishes_third(ac: AsyncClient):

    menu_data = (await ac.get(reverse(get_all_menus))).json()[0]
    menu_id = menu_data['id']
    submenu_data = (await ac.get(reverse(get_submenus, menu_id=menu_id))).json()[0]
    submenu_id = submenu_data['id']

    response = await ac.get(reverse(get_dishes, menu_id=menu_id, submenu_id=submenu_id))

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK

    # check that response is empty list
    assert response.json() == []


@pytest.mark.asyncio(scope='session')
async def test_delete_submenu(ac: AsyncClient):

    menu_data = (await ac.get(reverse(get_all_menus))).json()[0]
    menu_id = menu_data['id']
    submenu_data = (await ac.get(reverse(get_submenus, menu_id=menu_id))).json()[0]
    submenu_id = submenu_data['id']

    response = await ac.delete(reverse(delete_submenu, menu_id=menu_id, submenu_id=submenu_id))

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK


@pytest.mark.asyncio(scope='session')
async def test_get_submenus(ac: AsyncClient):

    menu_data = (await ac.get(reverse(get_all_menus))).json()[0]
    menu_id = menu_data['id']

    submenu_data = (await ac.get(reverse(get_submenus, menu_id=menu_id)))

    # check that response status HTTP 200 OK
    assert submenu_data.status_code == HTTPStatus.OK

    # check that response is empty list
    assert submenu_data.json() == []


@pytest.mark.asyncio(scope='session')
async def test_delete_menu(ac: AsyncClient):

    menu_data = (await ac.get(reverse(get_all_menus))).json()[0]
    menu_id = menu_data['id']

    response = await ac.delete(
        reverse(delete_menu, menu_id=menu_id)
    )

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK


@pytest.mark.asyncio(scope='session')
async def test_get_menus(ac: AsyncClient):

    response = await ac.get(
        reverse(get_all_menus)
    )

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK

    # check that response is empty list
    assert response.json() == []
