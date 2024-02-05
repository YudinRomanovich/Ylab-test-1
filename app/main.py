from fastapi import FastAPI
from src.database.database_main import init_db
from src.dish.router import router as dish_router
from src.menu.router import router as menu_router
from src.submenu.router import router as submenu_router

app = FastAPI()


@app.on_event('startup')
async def on_startup():
    await init_db()


app.include_router(menu_router)
app.include_router(submenu_router)
app.include_router(dish_router)
