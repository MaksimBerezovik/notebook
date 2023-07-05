from typing import Protocol
from typing import Type
from typing import final
from uuid import UUID

import attrs

from ddd.contacts.entities.v1 import Contact
from ddd.contacts.entities.v1 import ContactData
from ddd.contacts.entities.v1 import ContactPatch
from ddd.contacts.entities.v1 import Contacts
from ddd.contacts.interfaces import Repository


class _UniqueMixinDeps(Protocol):
    repository: Repository
    AlreadyExists: Type[RuntimeError]


class UniqueMixin(_UniqueMixinDeps):
    def _ensure_unique_name(self, name: str | None) -> None:
        same_name = self.repository.find(
            [
                Repository.Filter(
                    field="name",
                    op="eq",
                    value=name,
                )
            ],
        )
        if same_name:
            msg = f"contact with {name=!r} already exists"
            raise self.AlreadyExists(msg)

    def _ensure_unique_phone(self, phone: str | None) -> None:
        same_phone = self.repository.find(
            [
                Repository.Filter(
                    field="phone",
                    op="eq",
                    value=phone,
                ),
            ]
        )
        if same_phone:
            msg = f"contact with {phone=!r} already exists"
            raise self.AlreadyExists(msg)


@final
@attrs.frozen
class CreateContactUseCase(UniqueMixin):
    repository: Repository

    class AlreadyExists(RuntimeError):
        pass

    def __call__(self, *, data: ContactData) -> Contact:
        self._ensure_unique_name(data.name)
        self._ensure_unique_phone(data.phone)

        contact_id = self.repository.create_one(data)
        contact = self.repository.read_one(contact_id)
        return contact


@final
@attrs.frozen
class ReadContactUseCase:
    repository: Repository

    class DoesNotExist(RuntimeError):
        pass

    def __call__(self, *, contact_id: UUID) -> Contact:
        try:
            contact = self.repository.read_one(contact_id)
        except Repository.DoesNotExist as exc:
            raise self.DoesNotExist(exc) from exc

        return contact


@final
@attrs.frozen
class ReadContactsUseCase:
    repository: Repository

    def __call__(self) -> Contacts:
        contacts_list = self.repository.read_all()
        contacts = Contacts(items=contacts_list)
        return contacts


@final
@attrs.frozen
class UpdateContactUseCase(UniqueMixin):
    repository: Repository

    class DoesNotExist(RuntimeError):
        pass

    class AlreadyExists(RuntimeError):
        pass

    def __call__(self, *, contact_id: UUID, patch: ContactPatch) -> Contact:
        try:
            existing = self.repository.read_one(contact_id)
        except Repository.DoesNotExist as exc:
            raise self.DoesNotExist(exc) from exc

        self._ensure_unique_name(patch.name)
        self._ensure_unique_name(patch.phone)

        dirty_data = existing.dict() | patch.dict(
            exclude_defaults=True,
            exclude_none=True,
            exclude_unset=True,
        )
        dirty = Contact.parse_obj(dirty_data)
        self.repository.update_one(dirty)

        try:
            updated = self.repository.read_one(contact_id)
        except Repository.DoesNotExist as exc:
            raise self.DoesNotExist(exc) from exc

        return updated


@final
@attrs.frozen
class DeleteContactUseCase:
    repository: Repository

    class DoesNotExist(RuntimeError):
        pass

    def __call__(self, *, contact_id: UUID) -> None:
        try:
            self.repository.delete_one(contact_id)
        except Repository.DoesNotExist as exc:
            raise self.DoesNotExist(exc) from exc


@final
@attrs.frozen
class DeleteContactsUseCase:
    repository: Repository

    def __call__(self) -> None:
        self.repository.delete_all()
