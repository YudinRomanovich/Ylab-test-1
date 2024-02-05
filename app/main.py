from database.database_main import init_db
from dish.router import router as dish_router
from fastapi import FastAPI
from menu.router import router as menu_router
from submenu.router import router as submenu_router

app = FastAPI()


@app.on_event('startup')
async def on_startup():
    """Выполняется при запуске приложения.
    Инициализирует БД и запускает задачу обновления БД."""
    await init_db()


app.include_router(menu_router)
app.include_router(submenu_router)
app.include_router(dish_router)
