import json
import sqlite3
import uuid
from typing import Any

from django.http import HttpRequest
from django.http import HttpResponse
from django.http import JsonResponse
from pydantic import BaseModel

from app_maksim_berezovik.contacts.get_path_db import get_writeble_dir_db


class Contact(BaseModel):
    user_id: int | None = None
    name: str | None = None
    phone: str | None = None


class ContactCreate(BaseModel):
    name: str
    phone: str


class ContactUpdate(BaseModel):
    name: str | None
    phone: str | None


class Contactlist(BaseModel):
    items: list[Contact]


def create_database() -> None:
    path = get_writeble_dir_db()
    conn = sqlite3.connect(path / "contactsMB_django.db")
    cur = conn.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS contacts(
    id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT ,
    user_id INTEGER UNIQUE ,
    name TEXT,
    phone TEXT);
    """
    )
    conn.commit()
    conn.close()


def connection_data_base() -> Any:
    path = get_writeble_dir_db()
    conn = sqlite3.connect(path / "contactsMB_django.db")
    return conn


def delete_all_records(request: HttpRequest) -> HttpResponse:
    conn = connection_data_base()
    cur = conn.cursor()
    cur.execute("DELETE FROM contacts")
    conn.commit()
    conn.close()
    return HttpResponse("Данные удалены")


def get_contact_list() -> JsonResponse:
    conn = connection_data_base()
    cur = conn.cursor()
    cont = cur.execute("SELECT * from contacts")
    contacts_res = cont.fetchall()  # list with tuple(Contact info)
    result_list = []
    for i, contact_info in enumerate(contacts_res):  # noqa: B007
        # all records in db
        contact = {
            # usern=1,
            "user_id": contact_info[1],
            "name": contact_info[2],
            "phone": contact_info[3],
        }
        result_list.append(contact)
    contacts_result = [{"items": result_list}]
    conn.close()
    return JsonResponse(contacts_result, safe=False)


def create_contact(request: HttpRequest) -> HttpResponse | JsonResponse:
    conn = connection_data_base()
    cur = conn.cursor()
    user_id: int = uuid.uuid4().time_low
    body: dict = json.loads(request.body)
    user_name = body.get("name")
    user_phone = body.get("phone")
    result_id = cur.execute(
        "SELECT id FROM contacts WHERE user_id = ?", (user_id,)
    )
    contact_flag_user_id = bool(len(result_id.fetchall()))
    if not contact_flag_user_id:
        result_phone = cur.execute(
            "SELECT id FROM contacts WHERE phone = ?", (user_phone,)
        )
        contact_flag_phone = bool(len(result_phone.fetchall()))
        if not contact_flag_phone:
            cur.execute(
                "INSERT INTO contacts(user_id, name, phone) VALUES(?,?,?)",
                (user_id, user_name, user_phone),
            )
            conn.commit()
            conn.close()
            contact: Contact = Contact(
                user_id=user_id, name=user_name, phone=user_phone
            )
            return JsonResponse(
                {
                    "user_id": contact.user_id,
                    "name": contact.name,
                    "phone": contact.phone,
                }
            )
    conn.close()
    return HttpResponse("Такой контакт уже существует")


def view_contact_record(
    request: HttpRequest, user_id: int
) -> HttpResponse | JsonResponse:
    conn = connection_data_base()
    cur = conn.cursor()
    contact_id = user_id
    result_id = cur.execute(
        "SELECT id FROM contacts WHERE user_id = ?", (contact_id,)
    )
    contact_flag = bool(len(result_id.fetchall()))
    if not contact_flag:
        return HttpResponse("Такой контакт не найден")
    result = cur.execute(
        "SELECT * FROM contacts WHERE user_id = ?", (contact_id,)
    )
    contact = result.fetchall()[0]  # tuple with data of user_id
    resp: Contact = Contact(
        # usern=1,
        user_id=contact[1],
        name=contact[2],
        phone=contact[3],
    )
    conn.close()
    return JsonResponse(
        {"user_id": resp.user_id, "name": resp.name, "phone": resp.phone}
    )


def update_contact(request: HttpRequest, user_id: int) -> JsonResponse:
    conn = connection_data_base()
    cur = conn.cursor()
    body = json.loads(request.body)
    user_name = body["name"]
    user_phone = body["phone"]
    # check contact on DB
    result_id = cur.execute(
        "SELECT id FROM contacts WHERE user_id = ?", (user_id,)
    )
    contact_flag = bool(len(result_id.fetchall()))
    if not contact_flag:
        return JsonResponse("Такой контакт не найдет")
    if user_name is None:
        cur.execute(
            "Update contacts set phone = ? WHERE user_id = ?",
            (user_phone, user_id),
        )
        conn.commit()
    elif user_phone is None:
        cur.execute(
            "Update contacts set name = ? WHERE user_id = ?",
            (user_name, user_id),
        )
        conn.commit()
    else:
        cur.execute(
            "Update contacts set name = ?, phone = ?  WHERE user_id = ?",
            (user_name, user_phone, user_id),
        )
        conn.commit()
    upd_contact = cur.execute(
        "SELECT * FROM contacts WHERE user_id = ?", (user_id,)
    )
    upd_contact = upd_contact.fetchall()[0]
    upd_contact_res = Contact(
        user_id=upd_contact[1], name=upd_contact[2], phone=upd_contact[3]
    )
    return JsonResponse(
        {
            "user_id": upd_contact_res.user_id,
            "name": upd_contact_res.name,
            "phone": upd_contact_res.phone,
        },
        status=201,
    )


def delete_contact(request: HttpRequest, user_id: int) -> HttpResponse:
    conn = connection_data_base()
    cur = conn.cursor()
    # запрашиваем id из БД контакста с user_id
    result_id = cur.execute(
        "SELECT id FROM contacts WHERE user_id = ?", (user_id,)
    )
    contact_flag = bool(len(result_id.fetchall()))
    if contact_flag:  # если есть такой контакт - удаляем
        cur.execute("DELETE from contacts WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()
        return HttpResponse()
    conn.close()
    return HttpResponse("Такого контакта не существует")


def handel_view_contacts() -> HttpResponse:
    create_database()
    return get_contact_list()


def handel_create_contact(request: HttpRequest) -> HttpResponse:
    return create_contact(request)


def handel_view_contact(request: HttpRequest, user_id: int) -> HttpResponse:
    return view_contact_record(request, user_id)


def handel_update_contact(request: HttpRequest, user_id: int) -> HttpResponse:
    return update_contact(request, user_id)


def handel_delete_contact(request: HttpRequest, user_id: int) -> HttpResponse:
    return delete_contact(request, user_id)
