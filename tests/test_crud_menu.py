import pytest
from typing import AsyncGenerator
from httpx._client import AsyncClient
from http import HTTPStatus

from tests.services import reverse

from src.menu.router import (
    get_menu,
    get_all_menus,
    update_menu,
    create_menu,
    delete_menu
)


@pytest.mark.asyncio(scope='session')
async def test_get_menus(ac: AsyncGenerator[AsyncClient, None]) -> None:
    response = await ac.get(
        reverse(get_all_menus),
    )
    assert response.status_code == HTTPStatus.OK, \
        'Response not 200'
    assert response.json() == [], 'Responce not empty list'


@pytest.mark.asyncio(scope='session')
async def test_create_menu(ac: AsyncGenerator[AsyncClient, None], menu_post: dict[str, str]) -> None:

    response = await ac.post(
        reverse(create_menu),
        json=menu_post,
    )
    
    # check that response status HTTP 201 CREATED
    assert response.status_code == HTTPStatus.CREATED

    assert 'id' in response.json()

    assert 'title' in response.json()

    assert 'description' in response.json()

    assert 'submenus_count' in response.json()

    assert 'dishes_count' in response.json()

    assert response.json()['title'] == menu_post['title']

    assert response.json()['description'] == menu_post['description']


@pytest.mark.asyncio(scope='session')
async def test_get_menus_two(ac: AsyncGenerator[AsyncClient, None]) -> None:

    response = await ac.get(
        reverse(get_all_menus)
    )

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK

    # check that response is empty list
    assert not response.json() == [], "Response is empty list"


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
    assert response.json()["title"] == menu_data["title"]

    # check that 'dishes_count' from environment & response are equal
    assert response.json()["description"] == menu_data["description"]


@pytest.mark.asyncio(scope='session')
async def test_update_menu(ac: AsyncGenerator[AsyncClient, None], menu_patch: dict[str, str]):

    menu_data = (await ac.get(reverse(get_all_menus))).json()[0]
    menu_id = menu_data['id']
    
    response = await ac.patch(
        reverse(update_menu, menu_id=menu_id),
        json=menu_patch
    )

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK

    # check that 'menu_title' from environment & response are not equal
    assert not response.json()["title"] == menu_data["title"]

    # check that 'menu_description' from environment & response are not equal
    assert not response.json()["description"] == menu_data["description"]

    menu_data = await ac.get(
        reverse(get_menu, menu_id=menu_id)
    )

    # check that 'menu_title' from environment & response are equal
    assert response.json()["title"] == menu_data.json()["title"]

    # check that 'menu_description' from environment & response are equal
    assert response.json()["description"] == menu_data.json()["description"]


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
    assert response.json()["title"] == menu_data["title"]

    # check that 'dishes_count' from environment & response are equal
    assert response.json()["description"] == menu_data["description"]


@pytest.mark.asyncio(scope='session')
async def test_delete_menu(ac: AsyncGenerator[AsyncClient, None]):
    
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

    assert menu_data.json()['detail'] == "menu not found"


@pytest.mark.asyncio(scope='session')
async def test_get_menus_last(ac: AsyncGenerator[AsyncClient, None]):

    response = await ac.get(
        reverse(get_all_menus)
    )

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK

    # check that response is empty list
    assert response.json() == []
