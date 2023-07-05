from typing import Callable
from typing import Dict
from urllib.parse import parse_qs

from framework.debugging import debug
from framework.exceptions import UnsupportedMethod
from framework.http import Method
from framework.http import Request
from framework.http import Response
from framework.routing import list_routers
from framework.telemetry import capture_exception
from framework.telemetry import configure_sentry
from webapp.exceptions import UnsupportedPath


@configure_sentry
async def application(  # noqa: CCR001
    scope: Dict,
    receive: Callable,
    send: Callable,
) -> None:
    if scope["type"] == "lifespan":  # pragma: no cover
        return

    if scope["path"].startswith("/~/alexander_sidorov/contacts"):
        from hw.alexander_sidorov.contacts.api import app

        return await app(scope, receive, send)

    if scope["path"].startswith("/~/egor_pyshny/contacts"):
        from hw.egor_pyshny.routing import app

        return await app(scope, receive, send)

    if scope["path"].startswith("/~/maksim_berezovik/contacts"):
        from hw.maksim_berezovik.contacts import app

        return await app(scope, receive, send)

    recv = await receive()
    if recv["type"] != "http.request":
        debug("no support", recv)
        return

    if scope["path"] in ("/livez", "/livez/"):
        await send(
            {
                "status": 200,
                "type": "http.response.start",
            }
        )

        await send(
            {
                "body": b"server is alive",
                "type": "http.response.body",
            }
        )

        return

    body: bytes | None

    try:
        method = Method.from_scope(scope)

        request = Request(
            body=recv["body"],
            method=method,
            params=parse_qs(scope["query_string"].decode()),
            path=scope["path"],
        )

        for main in list_routers():
            try:
                response = main(request)
                break
            except UnsupportedPath:
                continue
        else:
            response = Response.build_not_found(request)

        if not isinstance(response, Response):
            errmsg = (
                f"router {main.__module__}.{main.__name__}"
                f" returns {type(response)}, {Response} expected"
            )
            raise RuntimeError(errmsg)

        body = response.build_body()

    except UnsupportedMethod:
        response = Response(status=405)
        body = b'"method not allowed"'

    except Exception as exc:
        capture_exception(exc)
        response = Response.build_exception(exc)
        body = response.build_body()

    status = response.status
    if scope["method"] in (Method.HEAD.value, Method.OPTIONS.value):
        status = 204 if status in range(200, 300) else status
        body = None

    headers = {**response.headers}
    if body is not None:
        headers.update(
            {
                "Content-Type": "application/json",
            }
        )

    headers_list = [
        (header.encode("utf8"), value.encode("utf8"))
        for header, value in sorted(headers.items())
    ]

    await send(
        {
            "headers": headers_list,
            "status": status,
            "type": "http.response.start",
        }
    )

    if body is not None:
        await send(
            {
                "body": body,
                "type": "http.response.body",
            }
        )
