from pathlib import Path

_this_file = Path(__file__)
_resolved = False

DIR_ALPHA = _this_file.parent

DIR_APP = DIR_ALPHA.parent

DIR_SERVICES = DIR_APP.parent

DIR_REPO = DIR_SERVICES.parent

DIR_SCRIPTS = DIR_APP / "scripts"

DIR_LOCAL = DIR_APP / ".local"

DIR_TMP = Path("/app/.local/")
if not DIR_TMP.is_dir():
    DIR_TMP = DIR_LOCAL

DIR_DOCKER_CACHE = Path("/var/cache/app")

DIR_STATIC = (
    DIR_DOCKER_CACHE if DIR_DOCKER_CACHE.is_dir() else DIR_LOCAL
) / "django-static"
DIR_STATIC.mkdir(exist_ok=True)


def _resolve() -> None:
    global _resolved
    if _resolved:  # pragma: no cover
        return

    import sys
    from functools import partial

    this_module = sys.modules[__name__]

    names = dir(this_module)
    _getattr = partial(getattr, this_module)
    namespace = zip(names, map(_getattr, names))
    paths = filter(lambda _pair: isinstance(_pair[1], Path), namespace)

    for name, obj in paths:
        obj = obj.resolve()
        setattr(this_module, name, obj)

    _resolved = True


_resolve()

__all__ = (
    "DIR_ALPHA",
    "DIR_APP",
    "DIR_LOCAL",
    "DIR_REPO",
    "DIR_SCRIPTS",
    "DIR_SERVICES",
    "DIR_TMP",
)
