from typing import Callable

from src.main import app


def get_all_routes() -> dict[str, str]:
    routes = {}
    for route in app.routes:
        routes[route.endpoint.__name__] = route.path
    return routes


def reverse(
    func: Callable,
    routes: dict[str, str] = get_all_routes(),
    **kwargs
) -> str:
    path = routes[func.__name__]
    return path.format(**kwargs)
