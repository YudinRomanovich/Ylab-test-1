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
async def test_get_submenus(ac, buffer_data: dict[str, Any]):

    response = await ac.get(f"/api/v1/menus/{buffer_data['menu']['id']}/submenus")

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK
    
    # check that response is empty list
    assert response.json() == []    


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

    # check that 'submenu_title' from environment & response are equal
    assert response.json()["title"] == buffer_data["submenu"]["title"]

    # check that 'submenu_description' from environment & response are equal
    assert response.json()["description"] == buffer_data["submenu"]["description"]


@pytest.mark.asyncio(scope='session')
async def test_get_submenus(ac, buffer_data: dict[str, Any]):

    response = await ac.get(f"/api/v1/menus/{buffer_data['menu']['id']}/submenus")

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK
    
    # check that response is empty list
    assert not response.json() == []


@pytest.mark.asyncio(scope='session')
async def test_get_specific_submenu_first(ac, buffer_data: dict[str, Any]):

    response = await ac.get(f"/api/v1/menus/{buffer_data['menu']['id']}/submenus/{buffer_data['submenu']['id']}")

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK

    # check that 'submenu_id' from environment & response are equal
    assert response.json()["id"] == buffer_data["submenu"]["id"]

    # check that 'submenu_title' from environment & response are equal
    assert response.json()["title"] == buffer_data["submenu"]["title"]

    # check that 'submenu_description' from environment & response are equal
    assert response.json()["description"] == buffer_data["submenu"]["description"]


@pytest.mark.asyncio(scope='session')
async def test_update_submenu(ac, buffer_data: dict[str, Any]):
    
    json_data = {
        "title": "My updated submenu 1",
        "description": "My updated submenu description 1"
    }

    response = await ac.patch(f"/api/v1/menus/{buffer_data['menu']['id']}/submenus/{buffer_data['submenu']['id']}", json=json_data)

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK

    # check that 'submenu_title' from environment & response are not equal
    assert not response.json()["title"] == buffer_data["submenu"]["title"]

    # check that 'submenu_description' from environment & response are not equal
    assert not response.json()["description"] == buffer_data["submenu"]["description"]

    # update env vars
    buffer_data["submenu"]["title"] = response.json()["title"]
    buffer_data["submenu"]["description"] = response.json()["description"]

    # check that 'submenu_title' from environment & response are equal
    assert response.json()["title"] == buffer_data["submenu"]["title"]

    # check that 'submenu_description' from environment & response are equal
    assert response.json()["description"] == buffer_data["submenu"]["description"]


@pytest.mark.asyncio(scope='session')
async def test_get_specific_submenu_second(ac, buffer_data: dict[str, Any]):

    response = await ac.get(f"/api/v1/menus/{buffer_data['menu']['id']}/submenus/{buffer_data['submenu']['id']}")

    # check that response status HTTP 200 OK
    assert response.status_code == HTTPStatus.OK

    # check that 'submenu_id' from environment & response are equal
    assert response.json()["id"] == buffer_data["submenu"]["id"]

    # check that 'submenu_title' from environment & response are equal
    assert response.json()["title"] == buffer_data["submenu"]["title"]

    # check that 'submenu_description' from environment & response are equal
    assert response.json()["description"] == buffer_data["submenu"]["description"]


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
async def test_get_specific_submenu_third(ac, buffer_data: dict[str, Any]):

    response = await ac.get(f"/api/v1/menus/{buffer_data['menu']['id']}/submenus/{buffer_data['submenu']['id']}")

    # check that response status HTTP 404 NOT FOUND
    assert response.status_code == HTTPStatus.NOT_FOUND

    # check that default message & response are equal
    assert response.json() == {"detail": "submenu not found"}


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
