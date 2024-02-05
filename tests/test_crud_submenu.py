from http import HTTPStatus

import pytest
from httpx._client import AsyncClient
from services import reverse
from src.menu.router import create_menu, delete_menu, get_all_menus, get_menu
from src.submenu.router import (
    add_submenu,
    delete_submenu,
    get_submenu,
    get_submenus,
    update_submenu,
)


@pytest.mark.asyncio(scope='session')
async def test_create_menu(ac: AsyncClient, menu_post: dict[str, str]) -> None:

    response = await ac.post(
        reverse(create_menu),
        json=menu_post,
    )

    # check that response status HTTP 201 CREATED
    assert response.status_code == HTTPStatus.CREATED

    assert 'id' in response.json()


@pytest.mark.asyncio(scope='session')
async def test_get_submenus_first(ac: AsyncClient):

    menu_data = (await ac.get(reverse(get_all_menus))).json()[0]
    menu_id = menu_data['id']

    response = await ac.get(reverse(get_submenus, menu_id=menu_id))

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK

    # check that response is empty list
    assert response.json() == []


@pytest.mark.asyncio(scope='session')
async def test_create_submenu(ac: AsyncClient, submenu_post: dict[str, str]):

    menu_data = (await ac.get(reverse(get_all_menus))).json()[0]
    menu_id = menu_data['id']

    response = await ac.post(reverse(add_submenu, menu_id=menu_id), json=submenu_post)

    # check that response status HTTP 201 CREATED
    assert response.status_code == HTTPStatus.CREATED

    submenu_data = (await ac.get(reverse(get_submenus, menu_id=menu_id))).json()[0]

    # check that 'submenu_id' from environment & response are equal
    assert response.json()['id'] == str(submenu_data['id'])

    # check that 'submenu_title' from environment & response are equal
    assert response.json()['title'] == submenu_data['title']

    # check that 'submenu_description' from environment & response are equal
    assert response.json()['description'] == submenu_data['description']


@pytest.mark.asyncio(scope='session')
async def test_get_submenus_second(ac: AsyncClient):

    menu_data = (await ac.get(reverse(get_all_menus))).json()[0]
    menu_id = menu_data['id']

    submenu_data = (await ac.get(reverse(get_submenus, menu_id=menu_id)))

    # check that response status HTTP 200 OK
    assert submenu_data.status_code == HTTPStatus.OK

    # check that response is not empty list
    assert not submenu_data == []


@pytest.mark.asyncio(scope='session')
async def test_get_specific_submenu_first(ac: AsyncClient):

    menu_data = (await ac.get(reverse(get_all_menus))).json()[0]
    menu_id = menu_data['id']
    submenu_data = (await ac.get(reverse(get_submenus, menu_id=menu_id))).json()[0]
    submenu_id = submenu_data['id']

    response = await ac.get(reverse(get_submenu, menu_id=menu_id, submenu_id=submenu_id))

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK

    # check that 'submenu_id' from environment & response are equal
    assert response.json()['id'] == str(submenu_data['id'])

    # check that 'submenu_title' from environment & response are equal
    assert response.json()['title'] == submenu_data['title']

    # check that 'submenu_description' from environment & response are equal
    assert response.json()['description'] == submenu_data['description']


@pytest.mark.asyncio(scope='session')
async def test_update_submenu(ac: AsyncClient, submenu_patch: dict[str, str]):

    menu_data = (await ac.get(reverse(get_all_menus))).json()[0]
    menu_id = menu_data['id']
    submenu_data = (await ac.get(reverse(get_submenus, menu_id=menu_id))).json()[0]
    submenu_id = submenu_data['id']

    response = await ac.patch(reverse(update_submenu, menu_id=menu_id, submenu_id=submenu_id), json=submenu_patch)

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK

    # check that 'submenu_title' from environment & response are not equal
    assert not response.json()['title'] == submenu_data['title']

    # check that 'submenu_description' from environment & response are not equal
    assert not response.json()['description'] == submenu_data['description']

    # update env vars
    submenu_data = (await ac.get(reverse(get_submenus, menu_id=menu_id))).json()[0]

    # check that 'submenu_title' from environment & response are equal
    assert response.json()['title'] == submenu_data['title']

    # check that 'submenu_description' from environment & response are equal
    assert response.json()['description'] == submenu_data['description']


@pytest.mark.asyncio(scope='session')
async def test_get_specific_submenu_second(ac: AsyncClient):

    menu_data = (await ac.get(reverse(get_all_menus))).json()[0]
    menu_id = menu_data['id']
    submenu_data = (await ac.get(reverse(get_submenus, menu_id=menu_id))).json()[0]
    submenu_id = submenu_data['id']

    response = await ac.get(reverse(get_submenu, menu_id=menu_id, submenu_id=submenu_id))

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK

    # check that 'submenu_id' from environment & response are equal
    assert response.json()['id'] == str(submenu_data['id'])

    # check that 'submenu_title' from environment & response are equal
    assert response.json()['title'] == submenu_data['title']

    # check that 'submenu_description' from environment & response are equal
    assert response.json()['description'] == submenu_data['description']


@pytest.mark.asyncio(scope='session')
async def test_delete_submenu(ac: AsyncClient):

    menu_data = (await ac.get(reverse(get_all_menus))).json()[0]
    menu_id = menu_data['id']
    submenu_data = (await ac.get(reverse(get_submenus, menu_id=menu_id))).json()[0]
    submenu_id = submenu_data['id']

    response = await ac.delete(reverse(delete_submenu, menu_id=menu_id, submenu_id=submenu_id))

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK

    response = (await ac.get(reverse(get_submenu, menu_id=menu_id, submenu_id=submenu_id)))

    # check that response status HTTP 404 NOT FOUND
    assert response.status_code == HTTPStatus.NOT_FOUND

    # check that "submenu" is not exist
    assert response.json()['detail'] == 'submenu not found'


@pytest.mark.asyncio(scope='session')
async def test_get_submenus_third(ac: AsyncClient):

    menu_data = (await ac.get(reverse(get_all_menus))).json()[0]
    menu_id = menu_data['id']

    submenu_data = (await ac.get(reverse(get_submenus, menu_id=menu_id)))

    # check that response status HTTP 200 OK
    assert submenu_data.status_code == HTTPStatus.OK

    # check that response is not empty list
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

    menu_data = await ac.get(
        reverse(get_menu, menu_id=menu_id)
    )

    assert menu_data.json()['detail'] == 'menu not found'


@pytest.mark.asyncio(scope='session')
async def test_get_menus(ac: AsyncClient):

    response = await ac.get(
        reverse(get_all_menus),
    )
    assert response.status_code == HTTPStatus.OK, \
        'Response not 200'
    assert response.json() == [], 'Responce not empty list'
