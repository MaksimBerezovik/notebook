from typing import Sequence
from typing import final
from uuid import UUID
from uuid import uuid4

from app_alexander_sidorov import models
from ddd.contacts.entities.v1 import Contact
from ddd.contacts.entities.v1 import ContactData
from ddd.contacts.repositories import Repository


@final
class SqlRepository(Repository):
    def read_all(self) -> list[Contact]:
        contacts = [
            Contact.from_orm(record)
            for record in models.Contact.objects.order_by("name").all()
        ]
        return contacts

    def find(self, filters: Sequence[Repository.Filter]) -> list[Contact]:
        records = models.Contact.objects.order_by("name").all()

        filter_attrs = {fl.field: fl.value for fl in filters if fl.op == "eq"}
        if filter_attrs:
            records = records.filter(**filter_attrs)

        contacts = [Contact.from_orm(record) for record in records]

        return contacts

    def read_one(self, contact_id: UUID) -> Contact:
        try:
            record = models.Contact.objects.get(pk=contact_id)
            contact = Contact.from_orm(record)
            return contact
        except models.Contact.DoesNotExist as exc:
            msg = f"contact with id={contact_id} does not exist"
            raise Repository.DoesNotExist(msg) from exc

    def create_one(self, data: ContactData) -> UUID:
        record = models.Contact(
            pk=uuid4(),
            **data.dict(),
        )
        record.save()
        return record.pk

    def update_one(self, contact: Contact) -> None:
        nr = models.Contact.objects.filter(pk=contact.id).update(
            **contact.dict()
        )
        if not nr:
            msg = f"contact with id={contact.id} does not exist"
            raise Repository.DoesNotExist(msg)

    def delete_one(self, contact_id: UUID) -> None:
        nr, _ = models.Contact.objects.filter(pk=contact_id).delete()
        if not nr:
            msg = f"contact with id={contact_id} does not exist"
            raise Repository.DoesNotExist(msg)

    def delete_all(self) -> None:
        models.Contact.objects.all().delete()
