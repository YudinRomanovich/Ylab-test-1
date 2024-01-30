import pytest
from typing import AsyncGenerator
from httpx._client import AsyncClient
from http import HTTPStatus

from src.menu.utils import get_menus
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
    menu_data = await get_menus(menu_id=str(data['id']), session=override_get_async_session)

    assert menu_data is not None

    # check that 'menu_id' from environment & response are equal
    assert response.json()["id"] == menu_data["id"]


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


@pytest.mark.asyncio(scope='session')
async def test_get_dishes_first(ac: AsyncGenerator[AsyncClient, None], override_get_async_session):

    menu_id = (await get_menus(session=override_get_async_session))[0]['id']
    submenu_id = (await get_submenus(menu_id=menu_id, session=override_get_async_session))[0]['id']

    response = await ac.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes")

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK

    dishes_data = await get_dishes(submenu_id=submenu_id, session=override_get_async_session)

    # check that response is empty list
    assert dishes_data == []


@pytest.mark.asyncio(scope='session')
async def test_create_dish(ac: AsyncGenerator[AsyncClient, None], override_get_async_session):

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

    dishes_data = await get_dishes(submenu_id=submenu_id, dish_id=dish_id, session=override_get_async_session)

    # check that 'dish_id' from environment & response are equal
    assert response.json()["id"] == str(dishes_data["id"])

    # check that 'dish_title' from environment & response are equal
    assert response.json()["title"] == dishes_data["title"]

    # check that 'dish_description' from environment & response are equal
    assert response.json()["description"] == dishes_data["description"]

    # check that 'dish_price' from environment & response are equal
    assert response.json()["price"] == dishes_data["price"]


@pytest.mark.asyncio(scope='session')
async def test_get_dishes_second(ac: AsyncGenerator[AsyncClient, None], override_get_async_session):

    menu_id = (await get_menus(session=override_get_async_session))[0]['id']
    submenu_id = (await get_submenus(menu_id=menu_id, session=override_get_async_session))[0]['id']

    response = await ac.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes")

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK

    dishes_data = await get_dishes(submenu_id=submenu_id, session=override_get_async_session)

    # check that response is empty list
    assert not dishes_data == []


@pytest.mark.asyncio(scope='session')
async def test_get_specific_dish_first(ac: AsyncGenerator[AsyncClient, None], override_get_async_session):

    menu_id = (await get_menus(session=override_get_async_session))[0]['id']
    submenu_id = (await get_submenus(menu_id=menu_id, session=override_get_async_session))[0]['id']
    dish_data = (await get_dishes(submenu_id=submenu_id, session=override_get_async_session))[0]

    response = await ac.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_data['id']}")

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK

    # check that 'dish_id' from environment & response are equal
    assert response.json()["id"] == str(dish_data["id"])

    # check that 'dish_title' from environment & response are equal
    assert response.json()["title"] == dish_data["title"]

    # check that 'dish_description' from environment & response are equal
    assert response.json()["description"] == dish_data["description"]

    # check that 'dish_price' from environment & response are equal
    assert response.json()["price"] == dish_data["price"]


@pytest.mark.asyncio(scope='session')
async def test_update_dish(ac: AsyncGenerator[AsyncClient, None], override_get_async_session):

    menu_id = (await get_menus(session=override_get_async_session))[0]['id']
    submenu_id = (await get_submenus(menu_id=menu_id, session=override_get_async_session))[0]['id']
    dish_data = (await get_dishes(submenu_id=submenu_id, session=override_get_async_session))[0]
    
    json_data = {
        "title": "My updated dish 1",
        "description": "My updated dish description 1",
        "price": "14.50"
    }

    response = await ac.patch(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_data['id']}", json=json_data)

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK 

    # check that 'dish_title' from environment & response are not equal
    assert not response.json()["title"] == dish_data["title"]

    # check that 'dish_description' from environment & response are not equal
    assert not response.json()["description"] == dish_data["description"]

    # check that 'dish_price' from environment & response are not equal
    assert not response.json()["price"] == dish_data["price"]

    dish_data = await get_dishes(submenu_id=submenu_id, dish_id=dish_data['id'], session=override_get_async_session)

    # check that 'dish_title' from environment & response are equal
    assert response.json()["title"] == dish_data["title"]

    # check that 'dish_description' from environment & response are equal
    assert response.json()["description"] == dish_data["description"]

    # check that 'dish_price' from environment & response are equal
    assert response.json()["price"] == dish_data["price"]


@pytest.mark.asyncio(scope='session')
async def test_get_specific_dish_second(ac: AsyncGenerator[AsyncClient, None], override_get_async_session):

    menu_id = (await get_menus(session=override_get_async_session))[0]['id']
    submenu_id = (await get_submenus(menu_id=menu_id, session=override_get_async_session))[0]['id']
    dish_data = (await get_dishes(submenu_id=submenu_id, session=override_get_async_session))[0]

    response = await ac.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_data['id']}")

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK

    # check that 'dish_id' from environment & response are equal
    assert response.json()["id"] == str(dish_data["id"])

    # check that 'dish_title' from environment & response are equal
    assert response.json()["title"] == dish_data["title"]

    # check that 'dish_description' from environment & response are equal
    assert response.json()["description"] == dish_data["description"]

    # check that 'dish_price' from environment & response are equal
    assert response.json()["price"] == dish_data["price"]


@pytest.mark.asyncio(scope='session')
async def test_delete_dish(ac: AsyncGenerator[AsyncClient, None], override_get_async_session, saved_id_data):

    menu_id = (await get_menus(session=override_get_async_session))[0]['id']
    submenu_id = (await get_submenus(menu_id=menu_id, session=override_get_async_session))[0]['id']
    dish_id = (await get_dishes(submenu_id=submenu_id, session=override_get_async_session))[0]['id']
    saved_id_data['dish'] = dish_id

    response = await ac.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK


@pytest.mark.asyncio(scope='session')
async def test_get_dishes_third(ac: AsyncGenerator[AsyncClient, None], override_get_async_session):

    menu_id = (await get_menus(session=override_get_async_session))[0]['id']
    submenu_id = (await get_submenus(menu_id=menu_id, session=override_get_async_session))[0]['id']

    response = await ac.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes")

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK

    dish_data = await get_dishes(submenu_id=submenu_id, session=override_get_async_session)

    # check that response is empty list
    assert dish_data == []


# @pytest.mark.asyncio(scope='session')
# async def test_get_specific_dish_third(ac: AsyncGenerator[AsyncClient, None], override_get_async_session, saved_id_data):

#     menu_id = (await get_menus(session=override_get_async_session))[0]['id']
#     submenu_id = (await get_submenus(menu_id=menu_id, session=override_get_async_session))[0]['id']
#     dish_id = saved_id_data['dish']

#     response = await ac.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_data['id']}")

#     # check that response status HTTP 200 OK
#     assert response.status_code == HTTPStatus.NOT_FOUND

#     # check that 'dish_id' from environment & response are equal
#     assert response.json() == {"detail": "dish not found"}


@pytest.mark.asyncio(scope='session')
async def test_delete_submenu(ac: AsyncGenerator[AsyncClient, None], override_get_async_session):

    menu_id = (await get_menus(session=override_get_async_session))[0]['id']
    submenu_id = (await get_submenus(menu_id=menu_id, session=override_get_async_session))[0]['id']

    response = await ac.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK


@pytest.mark.asyncio(scope='session')
async def test_get_submenus(ac: AsyncGenerator[AsyncClient, None], override_get_async_session):

    menu_id = (await get_menus(session=override_get_async_session))[0]['id']

    response = await ac.get(f"/api/v1/menus/{menu_id}/submenus")

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK

    menu_data = await get_submenus(menu_id=menu_id, session=override_get_async_session)
    
    # check that response is empty list
    assert menu_data == []


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
