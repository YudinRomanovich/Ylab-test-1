import pytest

from http import HTTPStatus
from typing import Any


@pytest.mark.asyncio(scope='session')
async def test_create_menu(ac, buffer_data: dict[str, Any]):

    json_data = {
        "title": "My menu 1",
        "description": "My menu description 1"
    }

    response = await ac.post("/api/v1/menus/", json=json_data)
    
    # check that response status HTTP 201 CREATED
    assert response.status_code == HTTPStatus.CREATED

    # save env vars
    buffer_data.update(menu = response.json())

    # check that 'menu_id' from environment & response are equal
    assert response.json()["id"] == buffer_data["menu"]["id"]


@pytest.mark.asyncio(scope='session')
async def test_create_submenu(ac, buffer_data: dict[str, Any]):

    json_data = {
        "title": "My submenu 1",
        "description": "My submenu description 1"
    }

    response = await ac.post(f"/api/v1/menus/{buffer_data['menu']['id']}/submenus", json=json_data)    

    # check that response status HTTP 201 CREATED
    assert response.status_code == HTTPStatus.CREATED

    # save env vars
    buffer_data.update(submenu = response.json())

    # check that 'submenu_id' from environment & response are equal
    assert response.json()["id"] == buffer_data["submenu"]["id"]


@pytest.mark.asyncio(scope='session')
async def test_get_dishes_first(ac, buffer_data: dict[str, Any]):

    response = await ac.get(f"/api/v1/menus/{buffer_data['menu']['id']}/submenus/{buffer_data['submenu']['id']}/dishes")

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK

    # check that response is empty list
    assert response.json() == []


@pytest.mark.asyncio(scope='session')
async def test_create_dish(ac, buffer_data: dict[str, Any]):

    json_data = {
        "title": "My dish 1",
        "description": "My dish description 1",
        "price": "12.50"
    }

    response = await ac.post(f"/api/v1/menus/{buffer_data['menu']['id']}/submenus/{buffer_data['submenu']['id']}/dishes", json=json_data)

    # check that response status HTTP 201 CREATED
    assert response.status_code == HTTPStatus.CREATED

    # save env vars
    buffer_data.update(dish = response.json())

    # check that 'dish_id' from environment & response are equal
    assert response.json()["id"] == buffer_data["dish"]["id"]

    # check that 'dish_title' from environment & response are equal
    assert response.json()["title"] == buffer_data["dish"]["title"]

    # check that 'dish_description' from environment & response are equal
    assert response.json()["description"] == buffer_data["dish"]["description"]

    # check that 'dish_price' from environment & response are equal
    assert response.json()["price"] == buffer_data["dish"]["price"]


@pytest.mark.asyncio(scope='session')
async def test_get_dishes_second(ac, buffer_data: dict[str, Any]):

    response = await ac.get(f"/api/v1/menus/{buffer_data['menu']['id']}/submenus/{buffer_data['submenu']['id']}/dishes")

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK

    # check that response is empty list
    assert not response.json() == []


@pytest.mark.asyncio(scope='session')
async def test_get_specific_dish_first(ac, buffer_data: dict[str, Any]):

    response = await ac.get(f"/api/v1/menus/{buffer_data['menu']['id']}/submenus/{buffer_data['submenu']['id']}/dishes/{buffer_data['dish']['id']}")

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK

    # check that 'dish_id' from environment & response are equal
    assert response.json()["id"] == buffer_data["dish"]["id"]

    # check that 'dish_title' from environment & response are equal
    assert response.json()["title"] == buffer_data["dish"]["title"]

    # check that 'dish_description' from environment & response are equal
    assert response.json()["description"] == buffer_data["dish"]["description"]

    # check that 'dish_price' from environment & response are equal
    assert response.json()["price"] == buffer_data["dish"]["price"]


@pytest.mark.asyncio(scope='session')
async def test_update_dish(ac, buffer_data: dict[str, Any]):
    
    json_data = {
        "title": "My updated dish 1",
        "description": "My updated dish description 1",
        "price": "14.50"
    }

    response = await ac.patch(f"/api/v1/menus/{buffer_data['menu']['id']}/submenus/{buffer_data['submenu']['id']}/dishes/{buffer_data['dish']['id']}", json=json_data)

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK 

    # check that 'dish_title' from environment & response are not equal
    assert not response.json()["title"] == buffer_data["dish"]["title"]

    # check that 'dish_description' from environment & response are not equal
    assert not response.json()["description"] == buffer_data["dish"]["description"]

    # check that 'dish_price' from environment & response are not equal
    assert not response.json()["price"] == buffer_data["dish"]["price"]

    # update env vars
    buffer_data.update(dish = response.json())

    # check that 'dish_title' from environment & response are equal
    assert response.json()["title"] == buffer_data["dish"]["title"]

    # check that 'dish_description' from environment & response are equal
    assert response.json()["description"] == buffer_data["dish"]["description"]

    # check that 'dish_price' from environment & response are equal
    assert response.json()["price"] == buffer_data["dish"]["price"]


@pytest.mark.asyncio(scope='session')
async def test_get_specific_dish_second(ac, buffer_data: dict[str, Any]):

    response = await ac.get(f"/api/v1/menus/{buffer_data['menu']['id']}/submenus/{buffer_data['submenu']['id']}/dishes/{buffer_data['dish']['id']}")

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK

    # check that 'dish_id' from environment & response are equal
    assert response.json()["id"] == buffer_data["dish"]["id"]

    # check that 'dish_title' from environment & response are equal
    assert response.json()["title"] == buffer_data["dish"]["title"]

    # check that 'dish_description' from environment & response are equal
    assert response.json()["description"] == buffer_data["dish"]["description"]

    # check that 'dish_price' from environment & response are equal
    assert response.json()["price"] == buffer_data["dish"]["price"]


@pytest.mark.asyncio(scope='session')
async def test_delete_dish(ac, buffer_data: dict[str, Any]):

    response = await ac.delete(f"/api/v1/menus/{buffer_data['menu']['id']}/submenus/{buffer_data['submenu']['id']}/dishes/{buffer_data['dish']['id']}")

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK


@pytest.mark.asyncio(scope='session')
async def test_get_dishes_third(ac, buffer_data: dict[str, Any]):

    response = await ac.get(f"/api/v1/menus/{buffer_data['menu']['id']}/submenus/{buffer_data['submenu']['id']}/dishes")

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK

    # check that response is empty list
    assert response.json() == []


@pytest.mark.asyncio(scope='session')
async def test_get_specific_dish_third(ac, buffer_data: dict[str, Any]):

    response = await ac.get(f"/api/v1/menus/{buffer_data['menu']['id']}/submenus/{buffer_data['submenu']['id']}/dishes/{buffer_data['dish']['id']}")

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.NOT_FOUND

    # check that 'dish_id' from environment & response are equal
    assert response.json() == {"detail": "dish not found"}


@pytest.mark.asyncio(scope='session')
async def test_delete_submenu(ac, buffer_data: dict[str, Any]):

    response = await ac.delete(f"/api/v1/menus/{buffer_data['menu']['id']}/submenus/{buffer_data['submenu']['id']}")

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK


@pytest.mark.asyncio(scope='session')
async def test_get_submenus(ac, buffer_data: dict[str, Any]):

    response = await ac.get(f"/api/v1/menus/{buffer_data['menu']['id']}/submenus")

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK
    
    # check that response is empty list
    assert response.json() == []


@pytest.mark.asyncio(scope='session')
async def test_delete_menu(ac, buffer_data: dict[str, Any]):

    response = await ac.delete(f"/api/v1/menus/{buffer_data['menu']['id']}")

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK


@pytest.mark.asyncio(scope='session')
async def test_get_menus(ac, buffer_data: dict[str, Any]):

    response = await ac.get("/api/v1/menus/")

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK

    # check that response is empty list
    assert response.json() == []

    buffer_data.clear()
