from typing import Sequence
from typing import final
from uuid import UUID
from uuid import uuid4

from ddd.contacts.entities.v1 import Contact
from ddd.contacts.entities.v1 import ContactData
from ddd.contacts.interfaces import Repository


@final
class InMemoryRepository:
    _storage: dict[UUID, Contact] = {}

    def read_all(self) -> list[Contact]:
        contacts = sorted(self._storage.values(), key=lambda _c: _c.name)
        return contacts

    def find(self, filters: Sequence[Repository.Filter]) -> list[Contact]:
        contacts = filter(lambda c: True, self.read_all())
        for fl in filters:
            if fl.op != "eq":
                continue
            contacts = filter(
                lambda c: hasattr(c, fl.field)
                and getattr(c, fl.field) == fl.value,
                contacts,
            )
        return list(contacts)

    def read_one(self, contact_id: UUID) -> Contact:
        if contact_id not in self._storage:
            msg = f"contact with id={contact_id} does not exist"
            raise Repository.DoesNotExist(msg)

        return self._storage[contact_id]

    def create_one(self, data: ContactData) -> UUID:
        contact_id = uuid4()
        contact = Contact(id=contact_id, **data.dict())
        self._storage[contact_id] = contact
        return contact_id

    def update_one(self, contact: Contact) -> None:
        self._storage[contact.id] = contact

    def delete_one(self, contact_id: UUID) -> None:
        try:
            del self._storage[contact_id]
        except KeyError as exc:
            msg = f"contact with id={contact_id} does not exist"
            raise Repository.DoesNotExist(msg) from exc

    def delete_all(self) -> None:
        self._storage.clear()
