from typing import TYPE_CHECKING
from typing import Any
from typing import Protocol
from typing import Sequence

import attrs

if TYPE_CHECKING:
    from uuid import UUID

    from ddd.contacts.entities.v1 import Contact
    from ddd.contacts.entities.v1 import ContactData


class UseCase(Protocol):
    def __call__(self, **kwargs: Any) -> Any:
        raise NotImplementedError


class Repository(Protocol):
    class RepositoryError(RuntimeError):
        pass

    class DoesNotExist(RepositoryError):
        pass

    @attrs.frozen
    class Filter:
        field: str
        op: str
        value: Any

    def read_all(self) -> list["Contact"]:
        ...

    def find(self, filters: Sequence[Filter]) -> list["Contact"]:
        ...

    def read_one(self, contact_id: "UUID") -> "Contact":
        ...

    def create_one(self, data: "ContactData") -> "UUID":
        ...

    def update_one(self, contact: "Contact") -> None:
        ...

    def delete_one(self, contact_id: "UUID") -> None:
        ...

    def delete_all(self) -> None:
        ...
