from typing import Any
from typing import Callable

import sentry_sdk
from sentry_sdk import capture_exception as _sentry_capture_exception
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from sentry_sdk.integrations.asyncio import AsyncioIntegration

from alpha.settings import Settings
from framework.debugging import debug


def configure_sentry(application: Callable) -> Callable:
    settings = Settings()
    if not settings.SENTRY_DSN:
        return application

    debug("Sentry will be enabled", settings.SENTRY_DSN)

    sentry_sdk.init(
        settings.SENTRY_DSN,
        environment=settings.ENVIRONMENT,
        integrations=[AsyncioIntegration()],
        release=settings.VERSION,
        request_bodies="small",
        send_default_pii=True,
        traces_sampler=traces_sampler,
    )
    application_traced = SentryAsgiMiddleware(application)
    return application_traced


def traces_sampler(sampling_context: dict) -> bool:
    if not (asgi_scope := sampling_context.get("asgi_scope")):
        return False

    if asgi_scope.get("type") != "http":
        return False

    path = asgi_scope.get("path")
    if path.startswith("/livez"):
        return False

    return True


def capture_exception(*args: Any, **kwargs: Any) -> Any:
    settings = Settings()
    if not settings.SENTRY_DSN:
        return None

    return _sentry_capture_exception(*args, **kwargs)
