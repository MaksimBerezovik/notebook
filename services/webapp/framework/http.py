import enum
import traceback
from dataclasses import dataclass
from dataclasses import field
from typing import Type
from urllib.parse import urlencode

import orjson
from pydantic.fields import Field
from pydantic.main import BaseModel

from framework.exceptions import UnsupportedMethod


@enum.unique
class Method(enum.Enum):
    DELETE = "DELETE"
    GET = "GET"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
    PATCH = "PATCH"
    POST = "POST"
    PUT = "PUT"

    @classmethod
    def from_scope(cls: Type["Method"], scope: dict) -> "Method":
        try:
            method = Method(scope["method"].upper())
            return method
        except ValueError as exc:
            raise UnsupportedMethod() from exc


@dataclass
class Request:
    method: Method
    path: str
    params: dict[str, list[str]] = field(default_factory=dict)
    body: bytes = b""


class Response(BaseModel):
    body: BaseModel | bytes | None = None
    status: int = 200
    headers: dict = Field(default_factory=dict)

    def build_body(self) -> bytes:
        if self.status == 204:
            return b""

        if isinstance(self.body, bytes):
            return self.body

        if isinstance(self.body, BaseModel):
            if isinstance(self.body, Response):
                self.status = self.body.status
                self.body = self.body.body
                return self.build_body()

            body: str | bytes = self.body.json()
            if isinstance(body, str):
                body = body.encode()
            return body

        return orjson.dumps(self.body)

    @classmethod
    def build_not_found(cls, request: Request) -> "Response":
        return cls(
            status=404,
            body=orjson.dumps(
                {
                    "description": "path not found on server",
                    "method": request.method.value,
                    "path": request.path,
                    "query": urlencode(request.params),
                }
            ),
        )

    @classmethod
    def build_exception(cls, exc: Exception) -> "Response":
        return cls(
            status=500,
            body=orjson.dumps(
                {
                    "exception": str(exc),
                    "tb": traceback.format_exc(),
                }
            ),
        )
