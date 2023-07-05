from pathlib import Path


def get_writeble_dir() -> Path:
    p1: Path = Path("/app/.local")
    if p1.is_dir():
        return p1
    p2: Path = Path(__file__)
    webapp = p2.parent.parent.parent
    local = webapp / ".local"
    return local
