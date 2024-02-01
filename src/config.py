from dotenv import load_dotenv
import os

load_dotenv()

API_URL = '/api/v1'
MENUS_URL = '/menus'
MENU_URL = '/menus/{menu_id}'
MENU_INFO_URL = '/info/{menu_id}'
SUBMENUS_URL = '/menus/{menu_id}/submenus'
SUBMENU_URL = '/menus/{menu_id}/submenus/{submenu_id}'
DISHES_URL = '/menus/{menu_id}/submenus/{submenu_id}/dishes'
DISH_URL = '/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}'


DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")