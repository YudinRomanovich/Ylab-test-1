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
    buffer_data["menu"]["submenus_count"] += 1

    # check that 'target_submenu_id' from environment & response are equal
    assert response.json()["id"] == buffer_data["submenu"]["id"]


@pytest.mark.asyncio(scope='session')
async def test_create_dish_first(ac, buffer_data: dict[str, Any]):

    json_data = {
        "title": "My dish 1",
        "description": "My dish description 1",
        "price": "12.50"
    }

    response = await ac.post(f"/api/v1/menus/{buffer_data['menu']['id']}/submenus/{buffer_data['submenu']['id']}/dishes", json=json_data)    

    # check that response status HTTP 201 CREATED
    assert response.status_code == HTTPStatus.CREATED

    # save env vars
    buffer_data.update(dish1 = response.json())
    buffer_data["submenu"]["dishes_count"] +=1
    buffer_data["menu"]["dishes_count"] +=1

    # check that 'dish_id' from environment & response are equal
    assert response.json()['id'] == buffer_data["dish1"]["id"]


@pytest.mark.asyncio(scope='session')
async def test_create_dish_second(ac, buffer_data: dict[str, Any]):

    json_data = {
        "title": "My dish 2",
        "description": "My dish description 2",
        "price": "13.50"
    }

    response = await ac.post(f"/api/v1/menus/{buffer_data['menu']['id']}/submenus/{buffer_data['submenu']['id']}/dishes", json=json_data)    

    # check that response status HTTP 201 CREATED
    assert response.status_code == HTTPStatus.CREATED

    # save env vars
    buffer_data.update(dish2 = response.json())
    buffer_data["submenu"]["dishes_count"] +=1
    buffer_data["menu"]["dishes_count"] +=1

    # check that 'dish_id' from environment & response are equal
    assert response.json()['id'] == buffer_data["dish2"]["id"]


@pytest.mark.asyncio(scope='session')
async def test_get_specific_menu(ac, buffer_data: dict[str, Any]):

    response = await ac.get(f"/api/v1/menus/{buffer_data['menu']['id']}")

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK

    # check that 'menu_id' from environment & response are equal
    assert response.json()["id"] == buffer_data["menu"]["id"]

    # check that 'submenus_count' from environment & response are equal
    assert response.json()["submenus_count"] == buffer_data["menu"]["submenus_count"]

    # check that 'dishes_count' from environment & response are equal
    assert response.json()["dishes_count"] == buffer_data["menu"]["dishes_count"]


@pytest.mark.asyncio(scope='session')
async def test_get_specific_submenu(ac, buffer_data: dict[str, Any]):

    response = await ac.get(f"/api/v1/menus/{buffer_data['menu']['id']}/submenus/{buffer_data['submenu']['id']}")

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK

    # check that 'submenu_id' from environment & response are equal
    assert response.json()["id"] == buffer_data["submenu"]["id"]

    # check that 'dishes_count' from environment & response are equal
    assert response.json()["dishes_count"] == buffer_data["submenu"]["dishes_count"]


@pytest.mark.asyncio(scope='session')
async def test_delete_submenu(ac, buffer_data: dict[str, Any]):

    response = await ac.delete(f"/api/v1/menus/{buffer_data['menu']['id']}/submenus/{buffer_data['submenu']['id']}")

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK

    buffer_data["menu"]["submenus_count"] -= 1

    buffer_data["menu"]["dishes_count"] -= buffer_data["submenu"]["dishes_count"]

    # buffer_data["submenu"] = []


@pytest.mark.asyncio(scope='session')
async def test_get_submenus(ac, buffer_data: dict[str, Any]):

    response = await ac.get(f"/api/v1/menus/{buffer_data['menu']['id']}/submenus")

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK
    
    # check that response is empty list
    assert response.json() == []


@pytest.mark.asyncio(scope='session')
async def test_get_dishes(ac, buffer_data: dict[str, Any]):

    response = await ac.get(f"/api/v1/menus/{buffer_data['menu']['id']}/submenus/{buffer_data['submenu']['id']}/dishes")

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK 

    # check that response is empty list
    assert response.json() == []


@pytest.mark.asyncio(scope='session')
async def test_get_specific_menu(ac, buffer_data: dict[str, Any]):

    response = await ac.get(f"/api/v1/menus/{buffer_data['menu']['id']}")

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK

    # check that 'menu_id' from environment & response are equal
    assert response.json()["id"] == buffer_data["menu"]["id"]

    # check that 'submenus_count' from environment & response are equal
    assert response.json()["submenus_count"] == buffer_data["menu"]["submenus_count"]

    # check that 'dishes_count' from environment & response are equal
    assert response.json()["dishes_count"] == buffer_data["menu"]["dishes_count"]


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
