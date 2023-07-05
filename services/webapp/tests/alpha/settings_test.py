import os
from unittest import mock

import pytest

from alpha.settings import Settings

pytestmark = [
    pytest.mark.unit,
]


default_settings = {
    "ENVIRONMENT": "local",
    "SECRET_KEY": "123",
    "VERSION": "dev",
}


@mock.patch.dict(os.environ, default_settings, clear=True)
def test_default_settings() -> None:
    settings = Settings()

    assert settings
