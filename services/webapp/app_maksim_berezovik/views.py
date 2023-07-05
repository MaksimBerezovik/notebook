from functools import partial
from typing import Any
from typing import Callable
from typing import Type
from typing import TypeVar

from django.http import HttpRequest
from django.http import HttpResponse
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from app_maksim_berezovik.contacts import usecases
from app_maksim_berezovik.contacts.contact_actions import ContactCreate
from app_maksim_berezovik.contacts.contact_actions import ContactUpdate
from app_maksim_berezovik.contacts.storages import Storage

Contact_model = TypeVar("Contact_model", ContactCreate, ContactUpdate)


def handle_hello_view(request: HttpRequest) -> HttpResponse:
    name = request.GET.get("name")
    if name:
        return HttpResponse(f"Hello {name} from Maksim Berezovik")
    return HttpResponse("Hello from Maksim Berezovik")


def get_payload(
    contact_model: Type[Contact_model], request: HttpRequest
) -> Contact_model | JsonResponse:
    try:
        payload = contact_model.parse_raw(request.body)
        return payload
    except ValueError as er:
        return JsonResponse(f"Error: {er}", status=422, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class ContactsView(View):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.__storage = Storage()
        self.__read_all = usecases.ReadAllContactsUseCase(
            storage=self.__storage
        )
        self.__read_one = usecases.ReadOneContactUseCase(
            storage=self.__storage
        )
        self.__update_contact = usecases.UpdateContactUseCase(
            storage=self.__storage
        )
        self.__create_contact = usecases.CreateContactsUseCase(
            storage=self.__storage
        )
        self.__delete_contact = usecases.DeleteContactUseCase(
            storage=self.__storage
        )

    def get(self, request: HttpRequest, **kw: Any) -> Any:
        subviews = [
            partial(meth, request)
            for meth in (
                self._read_all_contacts,
                self._read_singl_contact,
            )
        ]
        subview: Callable = subviews["contact_id" in kw]
        return subview(**kw)

    def _read_singl_contact(
        self, request: HttpRequest, **kw: Any
    ) -> JsonResponse:
        contact_id = kw["contact_id"]
        contact = self.__read_one(contact_id)
        return JsonResponse(contact.dict(), safe=False)

    def _read_all_contacts(
        self, request: HttpRequest, **kw: Any
    ) -> JsonResponse:
        assert request
        assert not kw
        contacts = self.__read_all()
        return JsonResponse(contacts.dict(), safe=False)

    def patch(self, request: HttpRequest, contact_id: int) -> JsonResponse:
        contact = get_payload(ContactUpdate, request)
        if isinstance(contact, JsonResponse):
            return contact
        contact_upd = self.__update_contact(
            contact_id=contact_id, **contact.dict()
        )
        if isinstance(contact_upd, JsonResponse):
            return contact_upd
        return JsonResponse(contact_upd.dict())

    def post(self, request: HttpRequest) -> JsonResponse:
        contact_body = get_payload(ContactCreate, request)
        if isinstance(contact_body, JsonResponse):
            return contact_body
        contact = self.__create_contact(contact_body=contact_body)
        return JsonResponse(contact.dict())

    def delete(self, request: HttpRequest, contact_id: int) -> HttpResponse:
        response = self.__delete_contact(contact_id=contact_id)
        return HttpResponse(status=response)
