import logging

import dj_database_url

from alpha import dirs
from alpha.settings import Settings as AlphaSettings  # noqa E131
from project.consts import TESTING_DB

alpha_settings = AlphaSettings()

SECRET_KEY = alpha_settings.SECRET_KEY

DEBUG = alpha_settings.MODE_DEBUG

ALLOWED_HOSTS: list[str] = [
    "127.0.0.1",
    "asgi",
    "localhost",
    "m-pt1-63-23.local",
    "m-pt1-63-23.local:8443",
    "m-pt1-63-23.sidorov.dev",
    "webapp",
]

CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://asgi",
    "http://localhost:8000",
    "https://m-pt1-63-23.local:8443",
    "https://m-pt1-63-23.sidorov.dev",
    "http://webapp",
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "rest_framework",
    "app_alexander_sidorov.apps.AppAlexanderSidorovConfig",
    "app_dmitriy_zhdanovich.apps.AppDmitriyZhdanovichConfig",
    "app_maksim_berezovik.apps.AppMaksimBerezovikConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"

_db_url = alpha_settings.DATABASE_URL
if not _db_url:
    logging.warning("DB is not configured: in-memory SQLite will be used")
    _db_url = "sqlite://"
assert isinstance(_db_url, str)

DATABASES = {
    "default": dj_database_url.parse(_db_url),
    "testing": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": TESTING_DB.as_posix(),
    },
}
DATABASE_ROUTERS = ["project.db_routers.DbRouter"]

_validators = "django.contrib.auth.password_validation"
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": f"{_validators}.UserAttributeSimilarityValidator",
    },
    {
        "NAME": f"{_validators}.MinimumLengthValidator",
    },
    {
        "NAME": f"{_validators}.CommonPasswordValidator",
    },
    {
        "NAME": f"{_validators}.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": {
            0: "whitenoise.storage.CompressedManifestStaticFilesStorage",
            1: "django.contrib.staticfiles.storage.StaticFilesStorage",
        }[DEBUG],
    },
}

STATIC_URL = "static/"

STATIC_ROOT = dirs.DIR_STATIC

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGGING = {
    "version": 1,
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
        }
    },
    # "loggers": {
    #     "django.db.backends": {
    #         "level": "DEBUG",
    #         "handlers": ["console"],
    #     }
    # },
}
