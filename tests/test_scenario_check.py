import pytest
from typing import AsyncGenerator
from httpx._client import AsyncClient
from http import HTTPStatus

from src.menu.utils import get_menus, get_menu_info
from src.submenu.utils import get_submenus
from src.dish.utils import get_dishes


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

    # check that 'submenu_id' from environment & response are equal
    assert response.json()["id"] == str(submenu_id)


@pytest.mark.asyncio(scope='session')
async def test_create_dish_first(ac: AsyncGenerator[AsyncClient, None], override_get_async_session):

    menu_id = (await get_menus(session=override_get_async_session))[0]['id']
    submenu_id = (await get_submenus(menu_id=menu_id, session=override_get_async_session))[0]['id']

    json_data = {
        "title": "My dish 1",
        "description": "My dish description 1",
        "price": "12.50"
    }

    response = await ac.post(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", json=json_data)

    # check that response status HTTP 201 CREATED
    assert response.status_code == HTTPStatus.CREATED

    dish_id = (await get_dishes(submenu_id=submenu_id, session=override_get_async_session))[0]['id']

    # check that 'dish_id' from environment & response are equal
    assert response.json()["id"] == str(dish_id)


@pytest.mark.asyncio(scope='session')
async def test_create_dish_second(ac: AsyncGenerator[AsyncClient, None], override_get_async_session):

    menu_id = (await get_menus(session=override_get_async_session))[0]['id']
    submenu_id = (await get_submenus(menu_id=menu_id, session=override_get_async_session))[0]['id']

    json_data = {
        "title": "My dish 2",
        "description": "My dish description 2",
        "price": "33.50"
    }

    response = await ac.post(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", json=json_data)

    # check that response status HTTP 201 CREATED
    assert response.status_code == HTTPStatus.CREATED

    dish_id = (await get_dishes(submenu_id=submenu_id, session=override_get_async_session))[1]['id']

    # check that 'dish_id' from environment & response are equal
    assert response.json()["id"] == str(dish_id)



@pytest.mark.asyncio(scope='session')
async def test_get_specific_menu(ac: AsyncGenerator[AsyncClient, None], override_get_async_session):

    menu_id = (await get_menus(session=override_get_async_session))[0]['id']

    response = await ac.get(f"/api/v1/menus/{menu_id}")

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK

    menu_data = (await get_menu_info(menu_id=menu_id, session=override_get_async_session))[0]

    # check that 'menu_id' from environment & response are equal
    assert response.json()["id"] == str(menu_data["id"])

    # check that 'submenus_count' from environment & response are equal
    assert response.json()["submenus_count"] == menu_data["submenus"]

    # check that 'dishes_count' from environment & response are equal
    assert response.json()["dishes_count"] == menu_data["dishes"]


@pytest.mark.asyncio(scope='session')
async def test_get_specific_submenu(ac: AsyncGenerator[AsyncClient, None], override_get_async_session):

    menu_id = (await get_menus(session=override_get_async_session))[0]['id']
    submenu_id = (await get_submenus(menu_id=menu_id, session=override_get_async_session))[0]['id']

    response = await ac.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK

    submenu_data = await get_submenus(menu_id=menu_id, submenu_id=submenu_id, session=override_get_async_session)

    # check that 'submenu_id' from environment & response are equal
    assert response.json()["id"] == str(submenu_data["id"])

    # check that 'dishes_count' from environment & response are equal
    assert response.json()["dishes_count"] == submenu_data["dishes_count"]


@pytest.mark.asyncio(scope='session')
async def test_delete_submenu(ac: AsyncGenerator[AsyncClient, None], override_get_async_session, saved_id_data):

    menu_id = (await get_menus(session=override_get_async_session))[0]['id']
    submenu_id = (await get_submenus(menu_id=menu_id, session=override_get_async_session))[0]['id']
    saved_id_data["submenu"] = submenu_id

    response = await ac.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK


@pytest.mark.asyncio(scope='session')
async def test_get_submenus(ac: AsyncGenerator[AsyncClient, None], override_get_async_session):

    menu_id = (await get_menus(session=override_get_async_session))[0]['id']

    response = await ac.get(f"/api/v1/menus/{menu_id}/submenus")

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK
    
    submenu_data = await get_submenus(menu_id=menu_id, session=override_get_async_session)

    # check that response is empty list
    assert submenu_data == []


@pytest.mark.asyncio(scope='session')
async def test_get_dishes(ac: AsyncGenerator[AsyncClient, None], override_get_async_session, saved_id_data):

    menu_id = (await get_menus(session=override_get_async_session))[0]['id']
    submenu_id = str(saved_id_data['submenu'])

    response = await ac.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes")

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK 

    dishes_data = await get_dishes(submenu_id=submenu_id, session=override_get_async_session)

    # check that response is empty list
    assert dishes_data == []


@pytest.mark.asyncio(scope='session')
async def test_get_specific_menu(ac: AsyncGenerator[AsyncClient, None], override_get_async_session):

    menu_id = (await get_menus(session=override_get_async_session))[0]['id']

    response = await ac.get(f"/api/v1/menus/{menu_id}")

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK

    menu_data = (await get_menu_info(menu_id=menu_id, session=override_get_async_session))[0]

    # check that 'menu_id' from environment & response are equal
    assert response.json()["id"] == str(menu_data["id"])

    # check that 'submenus_count' from environment & response are equal
    assert response.json()["submenus_count"] == menu_data["submenus"]

    # check that 'dishes_count' from environment & response are equal
    assert response.json()["dishes_count"] == menu_data["dishes"]


@pytest.mark.asyncio(scope='session')
async def test_delete_menu(ac: AsyncGenerator[AsyncClient, None], override_get_async_session):
    
    menu_data = (await get_menus(session=override_get_async_session))[0]

    response = await ac.delete(f"/api/v1/menus/{menu_data['id']}")

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK


@pytest.mark.asyncio(scope='session')
async def test_get_menus(ac: AsyncGenerator[AsyncClient, None], override_get_async_session):

    response = await ac.get("/api/v1/menus/")

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK

    menu_data = (await get_menus(session=override_get_async_session))

    # check that response is empty list
    assert menu_data == []
