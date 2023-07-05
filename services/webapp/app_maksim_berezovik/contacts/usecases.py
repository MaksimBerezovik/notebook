from typing import Any
from typing import Union
from typing import final
from uuid import uuid4

import attrs
from django.http import JsonResponse

from app_maksim_berezovik.contacts.contact_actions import Contactlist
from app_maksim_berezovik.contacts.storages import Storage


@final
@attrs.frozen(kw_only=True)
class ReadAllContactsUseCase:
    storage: Storage

    def __call__(self) -> Contactlist:
        items = list(self.storage.read_all())
        return Contactlist(items=items)


@final
@attrs.frozen(kw_only=True)
class ReadOneContactUseCase:
    storage: Storage

    def __call__(self, contact_id: int) -> Contactlist:
        item = self.storage.read_one(contact_id)
        return Contactlist(items=item)


@final
@attrs.frozen(kw_only=True)
class UpdateContactUseCase:
    storage: Storage

    def __call__(
        self, contact_id: int, **payload: Any
    ) -> Contactlist | JsonResponse:
        item: Union[list, JsonResponse] = self.storage.update_contact(
            contact_id, **payload
        )
        if isinstance(item, list):
            return Contactlist(items=item)
        return JsonResponse(item)


@final
@attrs.frozen(kw_only=True)
class CreateContactsUseCase:
    storage: Storage

    def __call__(self, contact_body: Any) -> Contactlist:
        contact_id: int = int(uuid4().time_low)
        item: Any = self.storage.create_contact(contact_id, contact_body)
        return Contactlist(items=item)


@final
@attrs.frozen(kw_only=True)
class DeleteContactUseCase:
    storage: Storage

    def __call__(self, contact_id: int) -> int:
        status = self.storage.delete_contact(contact_id)
        return status
