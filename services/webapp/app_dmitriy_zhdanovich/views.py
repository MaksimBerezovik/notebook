import json
from typing import Any

import orjson
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import View

from app_dmitriy_zhdanovich.models import Contacts
from hw.dmitriy_zhdanovich.contacts import UpdateContact


def handle_hello_world(request: HttpRequest) -> HttpResponse:
    if query := request.GET.get("name"):
        return HttpResponse(f"Hello {query} from Dmitriy Zhdanovich")
    return HttpResponse("Hello from Dmitriy Zhdanovich")


def python_data_structures_methods(
    request: HttpRequest, type_: str, meth: str
) -> HttpResponse | None:
    qs_dict: dict = request.GET
    types = {"str": str, "list": list, "dict": dict}
    obj: Any = qs_dict.get("obj")
    method = getattr(types[type_], meth)
    str_methods = [meth for meth in dir(str) if not meth.startswith("_")]
    list_methods = [meth for meth in dir(list) if not meth.startswith("_")]
    dict_methods = [meth for meth in dir(dict) if not meth.startswith("_")]
    if type_ == "str" and meth in str_methods:
        obj_form = method(obj)
        return HttpResponse(obj_form)
    elif type_ == "list" and meth in list_methods:
        if args := qs_dict.get("args"):
            method(json.loads(obj), args)
            return HttpResponse(json.dumps(obj))
        method(json.loads(obj))
        return HttpResponse(json.dumps(obj))
    elif type_ == "dict" and meth in dict_methods:
        if args := qs_dict.get("args"):
            return HttpResponse(json.dumps(method(json.loads(obj), args)))
        method(json.loads(obj))
        return HttpResponse(json.dumps(obj))
    return None


def validate(type_name: str, types: dict, meth: str, obj: Any) -> None:
    if not (type_name := types.get(type_name)):  # type: ignore
        raise TypeError("TypeError: unsupported type")
    if not hasattr(type_name, meth):
        raise ValueError(f"unknown method {type_name}.{meth}")
    if not isinstance(obj, type_name):
        raise ValueError(f"{obj} is not a {type_name}")
    return None


class CrudContacts(View):
    def get(
        self, request: HttpRequest, **kwargs: dict
    ) -> JsonResponse | HttpResponse:
        if kwargs:
            contact_id = kwargs["contact_id"]
            contact = get_object_or_404(Contacts, id=contact_id)
            contact_json = {
                "id": contact.id,
                "name": contact.name,
                "phone": contact.phone,
            }
            return JsonResponse(contact_json)
        contacts = list(Contacts.objects.all())
        contacts_json = [
            {"id": contact.id, "name": contact.name, "phone": contact.phone}
            for contact in contacts
        ]
        return JsonResponse(contacts_json, safe=False)

    def post(self, request: HttpRequest) -> JsonResponse:
        payload = orjson.loads(request.body)
        contact = Contacts(name=payload["name"], phone=payload["phone"])
        contact.save()

        return JsonResponse(
            {"id": contact.id, "name": contact.name, "phone": contact.phone},
            status=201,
        )

    def patch(
        self, request: HttpRequest, contact_id: int
    ) -> JsonResponse | HttpResponse:
        payload = UpdateContact.parse_raw(request.body)
        Contacts.objects.filter(id=contact_id).update(
            **payload.dict(exclude_unset=True)
        )
        contact = get_object_or_404(Contacts, id=contact_id)
        updated_contact_json = {
            "id": contact.id,
            "name": contact.name,
            "phone": contact.phone,
        }
        return JsonResponse(updated_contact_json)

    def delete(
        self, request: HttpRequest, contact_id: int
    ) -> JsonResponse | HttpResponse:
        get_object_or_404(Contacts, id=contact_id)
        Contacts.objects.filter(id=contact_id).delete()
        return JsonResponse({}, status=204)
