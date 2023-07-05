from typing import Any
from typing import Iterable

from django.http import JsonResponse

from app_maksim_berezovik.contacts.contact_actions import ContactCreate
from app_maksim_berezovik.models import Contact


class Storage:
    def read_all(self) -> list:
        items_obj: Iterable[Contact] = list(Contact.objects.all())
        items_list = [
            {
                "user_id": contact.user_id,
                "name": contact.name,
                "phone": contact.phone,
            }
            for contact in items_obj
        ]
        return items_list

    def read_one(self, contact_id: int) -> list:
        item_obj: Contact = Contact.objects.get(user_id=contact_id)
        item_list = [
            {
                "user_id": item_obj.user_id,
                "name": item_obj.name,
                "phone": item_obj.phone,
            }
        ]
        return item_list

    def update_contact(
        self, contact_id: int, **payload: Any
    ) -> list | JsonResponse:
        try:
            item_obj: Contact = Contact.objects.get(user_id=contact_id)
            if name := payload.get("name"):
                item_obj.name = name
                item_obj.save()
            elif phone := payload.get("phone"):
                item_obj.phone = phone
                item_obj.save()
            item_list = [
                {
                    "user_id": item_obj.user_id,
                    "name": item_obj.name,
                    "phone": item_obj.phone,
                }
            ]
            return item_list
        except Exception:
            return JsonResponse("contact not found", safe=False)

    def create_contact(
        self, contact_id: int, contact_body: ContactCreate
    ) -> dict:
        name = contact_body.name
        phone = contact_body.phone
        contact = Contact()
        contact.user_id = contact_id
        contact.name = name
        contact.phone = phone
        contact.save()

        item_list = {
            "user_id": contact.user_id,
            "name": contact.name,
            "phone": contact.phone,
        }

        return item_list

    def delete_contact(self, contact_id: int) -> int:
        # cont_id = contact_id
        Contact.objects.get(user_id=contact_id).delete()
        status = 200
        return status
