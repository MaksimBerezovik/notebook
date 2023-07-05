import sqlite3
import uuid
from typing import Any

import fastapi
from pydantic import BaseModel

from hw.maksim_berezovik import path_check


class Contact(BaseModel):
    user_id: int | None = None
    name: str | None = None
    phone: str | None = None


class Contactlist(BaseModel):
    items: list[Contact]


app = fastapi.FastAPI()
default_url = "/~/maksim_berezovik/contacts"


# create the database
def create_database() -> None:
    path = path_check.get_writeble_dir()
    conn = sqlite3.connect(path / "contactsMB.db")
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
    path = path_check.get_writeble_dir()
    conn = sqlite3.connect(path / "contactsMB.db")
    return conn


@app.get(f"{default_url}/delete")
def delete_all_records() -> str:
    conn = connection_data_base()
    cur = conn.cursor()
    cur.execute("DELETE FROM contacts")
    conn.commit()
    conn.close()
    return "База очищена"


def get_contact_list() -> Contactlist:
    conn = connection_data_base()
    cur = conn.cursor()
    cont = cur.execute("SELECT * from contacts")
    contacts_res = cont.fetchall()  # list with tuple(Contact info)
    result_list = []
    for i, contact_info in enumerate(contacts_res):  # noqa: B007
        # all records in db
        contact: Contact = Contact(
            # usern=1,
            user_id=contact_info[1],
            name=contact_info[2],
            phone=contact_info[3],
        )
        result_list.append(contact)
    contacts_result: Contactlist = Contactlist(items=result_list)
    conn.close()
    return contacts_result


@app.get(f"{default_url}")
def handler_view() -> Contactlist:
    create_database()
    return get_contact_list()


def view_contact_record(
    contact_id: int | str, response: fastapi.Response
) -> Contact | str:
    conn = connection_data_base()
    cur = conn.cursor()
    result_id = cur.execute(
        "SELECT id FROM contacts WHERE user_id = ?", (contact_id,)
    )
    contact_flag = bool(len(result_id.fetchall()))
    if not contact_flag:
        response.status_code = 404
        return "Такой контакт не найден"
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
    return resp


@app.get(f"{default_url}/{{user_id}}")
def handler_discription(
    user_id: int, response: fastapi.Response
) -> Contact | str:
    return view_contact_record(user_id, response)


def create_contact(item: Contact, response: fastapi.Response) -> Contact | str:
    conn = connection_data_base()
    cur = conn.cursor()
    user_id: int = uuid.uuid4().time_low
    new_contact = item
    new_contact.user_id = user_id
    # check contact on DB
    result_id = cur.execute(
        "SELECT id FROM contacts WHERE user_id = ?", (new_contact.user_id,)
    )
    contact_flag_user_id = bool(len(result_id.fetchall()))
    if not contact_flag_user_id:
        result_phone = cur.execute(
            "SELECT id FROM contacts WHERE phone = ?", (new_contact.phone,)
        )
        contact_flag_phone = bool(len(result_phone.fetchall()))
        if not contact_flag_phone:
            cur.execute(
                "INSERT INTO contacts(user_id, name, phone) VALUES(?,?,?)",
                (new_contact.user_id, new_contact.name, new_contact.phone),
            )
            conn.commit()
            conn.close()
            response.status_code = 201
            return new_contact
    conn.close()
    return "Такой контакт уже существует"


@app.post(f"{default_url}")
def handler_create_contact(
    item: Contact, response: fastapi.Response
) -> Contact | str:
    return create_contact(item, response)


def delete_contact(user_id: int, response: fastapi.Response) -> None | str:
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
        response.status_code = 204
        return None
    conn.close()
    response.status_code = 404
    return "Такого контакта не существует"


@app.delete(f"{default_url}/{{contact_id}}")
def handler_delete_contact(
    contact_id: int, response: fastapi.Response
) -> None | str:
    return delete_contact(contact_id, response)


def update_contact(
    contact_id: int, item: Contact, response: fastapi.Response
) -> Contact | str:
    conn = connection_data_base()
    cur = conn.cursor()
    # check contact on DB
    result_id = cur.execute(
        "SELECT id FROM contacts WHERE user_id = ?", (contact_id,)
    )
    contact_flag = bool(len(result_id.fetchall()))
    if not contact_flag:
        response.status_code = 404
        return "Такой контакт не найдет"
    if item.name is None:
        cur.execute(
            "Update contacts set phone = ? WHERE user_id = ?",
            (item.phone, contact_id),
        )
        conn.commit()
    if item.phone is None:
        cur.execute(
            "Update contacts set name = ? WHERE user_id = ?",
            (item.name, contact_id),
        )
        conn.commit()
    upd_contact = cur.execute(
        "SELECT * FROM contacts WHERE user_id = ?", (contact_id,)
    )
    upd_contact = upd_contact.fetchall()[0]
    upd_contact_res = Contact(
        user_id=upd_contact[1], name=upd_contact[2], phone=upd_contact[3]
    )
    return upd_contact_res


@app.patch(f"{default_url}/{{contact_id}}")
def handler_update_contact(
    contact_id: int, item: Contact, response: fastapi.Response
) -> Contact | str:
    return update_contact(contact_id, item, response)
