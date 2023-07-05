from typing import Any

from alpha.settings import Settings


class DbRouter:
    def db_for_read(self, model: Any, **hints: Any) -> str | None:
        settings = Settings()
        if settings.MODE_TESTING:
            return "testing"
        return None

    def db_for_write(self, model: Any, **hints: Any) -> str | None:
        settings = Settings()
        if settings.MODE_TESTING:
            return "testing"
        return None

    def allow_relation(self, obj1: Any, obj2: Any, **hints: Any) -> None:
        return None

    def allow_migrate(
        self,
        db: str,
        app_label: str,
        model_name: Any = None,
        **hints: Any,
    ) -> bool | None:
        if db == "testing":
            settings = Settings()
            return settings.MODE_TESTING
        return None
