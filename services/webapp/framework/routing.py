import importlib
from typing import Callable
from typing import Iterator

from alpha import dirs
from alpha.settings import Settings
from framework.http import Method
from framework.http import Request
from framework.http import Response

settings = Settings()


def list_routers() -> Iterator[Callable[[Request], Response]]:
    names = {
        "alexander_haiko",
        "alexander_sidorov",
        "anton_dmitruk",
        "dmitriy_zhdanovich",
        "egor_pyshny",
        "ilya_putrich",
        "maksim_berezovik",
        "nikita_harbatsevich",
        "vadim_zhurau",
        "victor_bushilo",
    }

    hw_path = dirs.DIR_APP / "hw"

    for pkg_dir in hw_path.glob("*"):
        if pkg_dir.name not in names:
            continue

        if not pkg_dir.is_dir():
            continue

        if not (pkg_dir / "__init__.py").is_file():
            continue

        if not (pkg_dir / "routing.py").is_file():
            continue

        routing = importlib.import_module(f"hw.{pkg_dir.name}.routing")

        if not hasattr(routing, "main"):
            continue

        yield routing.main

    yield handle_default


def handle_default(request: Request) -> Response:
    if request.path not in {"*", "/", ""} and request.method != Method.OPTIONS:
        from webapp.exceptions import UnsupportedPath

        raise UnsupportedPath

    response = Response(body=b"hi")

    if request.method == Method.OPTIONS:
        response.status = 204
        response.headers.update(
            {
                "Allow": ", ".join(sorted(meth.value for meth in Method)),
            }
        )

    return response
