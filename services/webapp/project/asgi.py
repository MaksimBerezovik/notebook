import os
from typing import Any
from typing import Callable

from django.core.asgi import get_asgi_application

from webapp.asgi import application as app_m63

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

app_django = get_asgi_application()


async def application(scope: dict, receive: Callable, send: Callable) -> Any:
    path: str = scope["path"]

    if path.startswith("/~"):
        return await app_m63(scope, receive, send)

    return await app_django(scope, receive, send)
