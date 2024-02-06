from fastapi import FastAPI

from src.database.database_main import init_db
from src.dish.router import router as dish_router
from src.menu.router import router as menu_router
from src.submenu.router import router as submenu_router

app = FastAPI(
    title='Ylab_app',
    version='0.1.0',
    openapi_tags=[
        {
            'name': 'Menu',
            'description': 'Actions with menu',
        },
        {
            'name': 'Submenu',
            'description': 'Actions with submenu',
        },
        {
            'name': 'Dishes',
            'description': 'Actions with dishes',
        },
    ]
)


@app.on_event('startup')
async def on_startup():
    await init_db()


app.include_router(menu_router)
app.include_router(submenu_router)
app.include_router(dish_router)
