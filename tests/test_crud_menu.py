import pytest
from typing import AsyncGenerator
from httpx._client import AsyncClient
from http import HTTPStatus

from src.menu.utils import get_menus

from src.config import MENU_URL, MENUS_URL, API_URL


@pytest.mark.asyncio(scope='session')
async def test_get_menus(ac: AsyncGenerator[AsyncClient, None], override_get_async_session):

    response = await ac.get(API_URL + MENUS_URL)

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK

    menu_data = await get_menus(session=override_get_async_session)
    # check that response is empty list
    assert response.json() == menu_data, "Response is not an empty list"


@pytest.mark.asyncio(scope='session')
async def test_create_menu(ac: AsyncGenerator[AsyncClient, None], override_get_async_session):

    json_data = {
        "title": "My menu 1",
        "description": "My menu description 1"
    }

    response = await ac.post(API_URL + MENUS_URL, json=json_data)
    
    # check that response status HTTP 201 CREATED
    assert response.status_code == HTTPStatus.CREATED

    data = response.json()

    # check that new record added to the database
    result = await get_menus(menu_id=str(data['id']), session=override_get_async_session)

    assert result is not None

    # check that 'menu_id' from environment & response are equal
    assert data["id"] == str(result["id"])

    # check that 'menu_title' from environment & response are equal
    assert data["title"] == result["title"]

    # check that 'menu_description' from environment & response are equal
    assert data["description"] == result["description"]


@pytest.mark.asyncio(scope='session')
async def test_get_menus_two(ac: AsyncGenerator[AsyncClient, None], override_get_async_session):

    response = await ac.get(API_URL + MENUS_URL)

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK

    menu_data = await get_menus(session=override_get_async_session)

    # check that response is empty list
    assert not response.json() == menu_data, "Response is empty list"


@pytest.mark.asyncio(scope='session')
async def test_get_specific_menu(ac: AsyncGenerator[AsyncClient, None], override_get_async_session):

    menu_data = (await get_menus(session=override_get_async_session))[0]

    response = await ac.get(f"/api/v1/menus/{menu_data['id']}")

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK

    # check that 'menu_id' from environment & response are equal
    assert response.json()["id"] == str(menu_data["id"])

    # check that 'submenus_count' from environment & response are equal
    assert response.json()["title"] == menu_data["title"]

    # check that 'dishes_count' from environment & response are equal
    assert response.json()["description"] == menu_data["description"]


@pytest.mark.asyncio(scope='session')
async def test_update_menu(ac: AsyncGenerator[AsyncClient, None], override_get_async_session):

    menu_data = (await get_menus(session=override_get_async_session))[0]
    
    json_data = {
        "title": "My updated menu 1",
        "description": "My updated menu description 1"
    }

    response = await ac.patch(f"/api/v1/menus/{menu_data['id']}", json=json_data)

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK

    # check that 'menu_title' from environment & response are not equal
    assert not response.json()["title"] == menu_data["title"]

    # check that 'menu_description' from environment & response are not equal
    assert not response.json()["description"] == menu_data["description"]

    menu_data = (await get_menus(session=override_get_async_session))[0]

    # check that 'menu_title' from environment & response are equal
    assert response.json()["title"] == menu_data["title"]

    # check that 'menu_description' from environment & response are equal
    assert response.json()["description"] == menu_data["description"]


@pytest.mark.asyncio(scope='session')
async def test_get_specific_menu(ac: AsyncGenerator[AsyncClient, None], override_get_async_session):

    menu_data = (await get_menus(session=override_get_async_session))[0]

    response = await ac.get(f"/api/v1/menus/{menu_data['id']}")

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK

    # check that 'menu_id' from environment & response are equal
    assert response.json()["id"] == str(menu_data["id"])

    # check that 'submenus_count' from environment & response are equal
    assert response.json()["title"] == menu_data["title"]

    # check that 'dishes_count' from environment & response are equal
    assert response.json()["description"] == menu_data["description"]


@pytest.mark.asyncio(scope='session')
async def test_delete_menu(ac: AsyncGenerator[AsyncClient, None], override_get_async_session):
    
    menu_id = (await get_menus(session=override_get_async_session))[0]['id']

    response = await ac.delete(f"/api/v1/menus/{menu_id}")

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK

    response = await ac.get(f"/api/v1/menus/{menu_id}")

    # check that response status HTTP 404 NOT FOUND
    assert response.status_code == HTTPStatus.NOT_FOUND

    menu_data = await get_menus(menu_id=menu_id, session=override_get_async_session)

    # check that 'menu_id' is not exist
    assert menu_data == "menu not found"



@pytest.mark.asyncio(scope='session')
async def test_get_menus(ac: AsyncGenerator[AsyncClient, None], override_get_async_session):

    response = await ac.get(API_URL + MENUS_URL)

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK

    menu_data = (await get_menus(session=override_get_async_session))

    # check that response is empty list
    assert menu_data == []
