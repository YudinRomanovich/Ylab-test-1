import pytest
from typing import AsyncGenerator
from httpx._client import AsyncClient
from http import HTTPStatus

from src.menu.utils import get_menus
from src.submenu.utils import get_submenus


@pytest.mark.asyncio(scope='session')
async def test_create_menu(ac: AsyncGenerator[AsyncClient, None], override_get_async_session):

    json_data = {
        "title": "My menu 1",
        "description": "My menu description 1"
    }

    response = await ac.post("/api/v1/menus/", json=json_data)
    
    # check that response status HTTP 201 CREATED
    assert response.status_code == HTTPStatus.CREATED

    data = response.json()

    # check that new record added to the database
    result = await get_menus(menu_id=str(data['id']), session=override_get_async_session)

    assert result is not None

    # check that 'menu_id' from environment & response are equal
    assert data["id"] == str(result["id"])


@pytest.mark.asyncio(scope='session')
async def test_get_submenus_first(ac: AsyncGenerator[AsyncClient, None], override_get_async_session):

    menu_id = (await get_menus(session=override_get_async_session))[0]['id']

    response = await ac.get(f"/api/v1/menus/{menu_id}/submenus")

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK
    
    submenu_data = await get_submenus(menu_id=menu_id, session=override_get_async_session)

    # check that response is empty list
    assert response.json() == submenu_data   


@pytest.mark.asyncio(scope='session')
async def test_create_submenu(ac: AsyncGenerator[AsyncClient, None], override_get_async_session):

    menu_id = (await get_menus(session=override_get_async_session))[0]['id']

    json_data = {
        "title": "My submenu 1",
        "description": "My submenu description 1"
    }

    response = await ac.post(f"/api/v1/menus/{menu_id}/submenus", json=json_data)    

    # check that response status HTTP 201 CREATED
    assert response.status_code == HTTPStatus.CREATED

    submenu_id = (await get_submenus(menu_id=menu_id, session=override_get_async_session))[0]['id']

    submenu_data = await get_submenus(menu_id=menu_id, submenu_id=submenu_id, session=override_get_async_session)

    # check that 'submenu_id' from environment & response are equal
    assert response.json()["id"] == str(submenu_data["id"])

    # check that 'submenu_title' from environment & response are equal
    assert response.json()["title"] == submenu_data["title"]

    # check that 'submenu_description' from environment & response are equal
    assert response.json()["description"] == submenu_data["description"]


@pytest.mark.asyncio(scope='session')
async def test_get_submenus_second(ac: AsyncGenerator[AsyncClient, None], override_get_async_session):

    menu_id = (await get_menus(session=override_get_async_session))[0]['id']

    response = await ac.get(f"/api/v1/menus/{menu_id}/submenus")

    submenu_data = await get_submenus(menu_id=menu_id, session=override_get_async_session)

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK
    
    # check that response is not empty list
    assert not submenu_data == []


@pytest.mark.asyncio(scope='session')
async def test_get_specific_submenu_first(ac: AsyncGenerator[AsyncClient, None], override_get_async_session):

    menu_id = (await get_menus(session=override_get_async_session))[0]['id']
    submenu_id = (await get_submenus(menu_id=menu_id, session=override_get_async_session))[0]['id']

    response = await ac.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK

    submenu_data = await get_submenus(menu_id=menu_id, submenu_id=submenu_id, session=override_get_async_session)

    # check that 'submenu_id' from environment & response are equal
    assert response.json()["id"] == str(submenu_data["id"])

    # check that 'submenu_title' from environment & response are equal
    assert response.json()["title"] == submenu_data["title"]

    # check that 'submenu_description' from environment & response are equal
    assert response.json()["description"] == submenu_data["description"]


@pytest.mark.asyncio(scope='session')
async def test_update_submenu(ac: AsyncGenerator[AsyncClient, None], override_get_async_session):

    menu_id = (await get_menus(session=override_get_async_session))[0]['id']
    submenu_data = (await get_submenus(menu_id=menu_id, session=override_get_async_session))[0]
    
    json_data = {
        "title": "My updated submenu 1",
        "description": "My updated submenu description 1"
    }

    response = await ac.patch(f"/api/v1/menus/{menu_id}/submenus/{submenu_data['id']}", json=json_data)

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK


    # check that 'submenu_title' from environment & response are not equal
    assert not response.json()["title"] == submenu_data["title"]

    # check that 'submenu_description' from environment & response are not equal
    assert not response.json()["description"] == submenu_data["description"]

    # update env vars
    submenu_data = await get_submenus(menu_id=menu_id, submenu_id=submenu_data['id'], session=override_get_async_session)

    # check that 'submenu_title' from environment & response are equal
    assert response.json()["title"] == submenu_data["title"]

    # check that 'submenu_description' from environment & response are equal
    assert response.json()["description"] == submenu_data["description"]


@pytest.mark.asyncio(scope='session')
async def test_get_specific_submenu_second(ac: AsyncGenerator[AsyncClient, None], override_get_async_session):

    menu_id = (await get_menus(session=override_get_async_session))[0]['id']
    submenu_id = (await get_submenus(menu_id=menu_id, session=override_get_async_session))[0]['id']

    response = await ac.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK

    submenu_data = await get_submenus(menu_id=menu_id, submenu_id=submenu_id, session=override_get_async_session)

    # check that 'submenu_id' from environment & response are equal
    assert response.json()["id"] == str(submenu_data["id"])

    # check that 'submenu_title' from environment & response are equal
    assert response.json()["title"] == submenu_data["title"]

    # check that 'submenu_description' from environment & response are equal
    assert response.json()["description"] == submenu_data["description"]


@pytest.mark.asyncio(scope='session')
async def test_delete_submenu(ac: AsyncGenerator[AsyncClient, None], override_get_async_session, saved_id_data):

    menu_id = (await get_menus(session=override_get_async_session))[0]['id']
    submenu_id = (await get_submenus(menu_id=menu_id, session=override_get_async_session))[0]['id']
    saved_id_data['submenu'] = submenu_id

    response = await ac.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK


@pytest.mark.asyncio(scope='session')
async def test_get_submenus_third(ac: AsyncGenerator[AsyncClient, None], override_get_async_session):

    menu_id = (await get_menus(session=override_get_async_session))[0]['id']

    response = await ac.get(f"/api/v1/menus/{menu_id}/submenus")

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK

    submenu_data = await get_submenus(menu_id=menu_id, session=override_get_async_session)
    
    # check that response is empty list
    assert submenu_data == []


@pytest.mark.asyncio(scope='session')
async def test_get_specific_submenu_third(ac: AsyncGenerator[AsyncClient, None], override_get_async_session, saved_id_data):

    menu_id = (await get_menus(session=override_get_async_session))[0]['id']
    submenu_id = str(saved_id_data['submenu'])

    response = await ac.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")

    # check that response status HTTP 404 NOT FOUND
    assert response.status_code == HTTPStatus.NOT_FOUND

    # check that default message & response are equal
    assert response.json() == {"detail": "submenu not found"}


@pytest.mark.asyncio(scope='session')
async def test_delete_menu(ac: AsyncGenerator[AsyncClient, None], override_get_async_session):

    menu_id = (await get_menus(session=override_get_async_session))[0]['id']

    response = await ac.delete(f"/api/v1/menus/{menu_id}")

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK


@pytest.mark.asyncio(scope='session')
async def test_get_menus(ac: AsyncGenerator[AsyncClient, None], override_get_async_session):

    response = await ac.get("/api/v1/menus/")

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK

    menu_data = await get_menus(session=override_get_async_session)

    # check that response is empty list
    assert menu_data == []
