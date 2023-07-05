from typing import Final

from alpha.dirs import DIR_TMP

TESTING_DB: Final = (DIR_TMP / "test.sqlite3").resolve()
