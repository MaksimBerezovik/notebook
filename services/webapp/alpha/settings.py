from pydantic.env_settings import BaseSettings

from alpha.dirs import DIR_APP


class Settings(BaseSettings):
    DATABASE_URL: str | None = None
    ENVIRONMENT: str
    MODE_DEBUG: bool = False
    MODE_TESTING: bool = False
    SECRET_KEY: str
    SENTRY_DSN: str | None = None
    TEST_SERVICE_URL: str = "http://localhost:8000"
    VERSION: str

    class Config:
        case_sensitive = True
        env_file = (DIR_APP / ".env.dist", DIR_APP / ".env")
        env_file_encoding = "utf-8"
