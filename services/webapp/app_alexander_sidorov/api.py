from functools import partial
from typing import Any
from typing import Type
from typing import TypeVar
from uuid import UUID

from django.http import Http404
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from pydantic.error_wrappers import ValidationError

from app_alexander_sidorov.repositories import SqlRepository
from ddd.contacts.entities.v1 import ContactData
from ddd.contacts.entities.v1 import ContactPatch
from ddd.contacts.usecases import CreateContactUseCase
from ddd.contacts.usecases import DeleteContactUseCase
from ddd.contacts.usecases import ReadContactsUseCase
from ddd.contacts.usecases import ReadContactUseCase
from ddd.contacts.usecases import UpdateContactUseCase

SchemaT = TypeVar(
    "SchemaT",
    ContactData,
    ContactPatch,
)


def payload_or_response(
    schema: Type[SchemaT],
    request: HttpRequest,
) -> SchemaT | JsonResponse:
    try:
        payload = schema.parse_raw(request.body)
        return payload
    except ValidationError as exc:
        return JsonResponse({"errors": exc.errors()}, status=422)


@method_decorator(csrf_exempt, name="dispatch")
class ContactsView(View):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.__repository = SqlRepository()
        self.__create = CreateContactUseCase(repository=self.__repository)
        self.__delete = DeleteContactUseCase(repository=self.__repository)
        self.__read_all = ReadContactsUseCase(repository=self.__repository)
        self.__read_one = ReadContactUseCase(repository=self.__repository)
        self.__update = UpdateContactUseCase(repository=self.__repository)

    def get(
        self,
        request: HttpRequest,
        **kw: Any,
    ) -> HttpResponse:
        subviews = [
            partial(meth, request)
            for meth in (
                self._read_all_contacts,
                self._read_single_contact,
            )
        ]

        subview = subviews["contact_id" in kw]
        return subview(**kw)

    def _read_all_contacts(
        self,
        request: HttpRequest,
        **kw: Any,
    ) -> JsonResponse:
        assert request
        assert not kw
        contacts = self.__read_all()
        return JsonResponse(contacts.dict())

    def _read_single_contact(
        self,
        request: HttpRequest,
        **kw: Any,
    ) -> JsonResponse:
        assert request
        contact_id: UUID = kw["contact_id"]
        try:
            contact = self.__read_one(contact_id=contact_id)
            return JsonResponse(contact.dict())
        except self.__read_one.DoesNotExist as exc:
            raise Http404() from exc

    def post(
        self,
        request: HttpRequest,
    ) -> JsonResponse:
        payload = payload_or_response(ContactData, request)
        if isinstance(payload, JsonResponse):
            return payload

        try:
            contact = self.__create(data=payload)
            return JsonResponse(contact.dict(), status=201)
        except self.__create.AlreadyExists as exc:
            return JsonResponse({"errors": [str(exc)]}, status=409)

    def patch(
        self,
        request: HttpRequest,
        contact_id: UUID,
    ) -> JsonResponse:
        payload = payload_or_response(ContactPatch, request)
        if isinstance(payload, JsonResponse):
            return payload

        try:
            contact = self.__update(contact_id=contact_id, patch=payload)
            return JsonResponse(contact.dict())
        except self.__update.DoesNotExist as exc:
            raise Http404 from exc
        except self.__update.AlreadyExists as exc:
            return JsonResponse({"errors": [str(exc)]}, status=409)

    def delete(
        self,
        request: HttpRequest,
        contact_id: UUID,
    ) -> HttpResponse:
        assert request

        try:
            self.__delete(contact_id=contact_id)
            return HttpResponse(status=204, content_type="application/json")
        except self.__delete.DoesNotExist as exc:
            raise Http404 from exc
