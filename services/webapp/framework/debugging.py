from contextlib import contextmanager
from datetime import datetime
from typing import Any
from typing import Callable
from typing import ParamSpec
from typing import TypeVar
from typing import cast

import devtools

from alpha.settings import Settings


def noop(*_args: Any, **_kw: Any) -> Any:
    return


debug = cast(Callable, devtools.debug if Settings().MODE_DEBUG else noop)

P = ParamSpec("P")  # noqa: VNE001
R = TypeVar("R")  # noqa: VNE001


def performance_meter_2000(func: Callable[P, R]) -> Callable[P, R]:
    def inner(*args: P.args, **kwargs: P.kwargs) -> R:
        t0 = datetime.now()
        try:
            return func(*args, **kwargs)
        finally:
            t1 = datetime.now()
            debug(func, t1 - t0)

    return inner


@contextmanager
def performance_meter_9000(description: str) -> Any:
    """
    class performance_meter_9000:
        def __init__(self, description: str):
            self._description = description
            self._t0 = None

        def __enter__(self):
            self._t0 = datetime.now()
            return "xxx"

        def __exit__(self, *args):
            t1 = datetime.now()
            dt = t1 - self._t0
            debug(description, dt)
    """

    t0 = datetime.now()
    try:
        yield "xxx"
    finally:
        t1 = datetime.now()
        dt = t1 - t0
        debug(description, dt)


__all__ = (
    "debug",
    "performance_meter_2000",
    "performance_meter_9000",
)
