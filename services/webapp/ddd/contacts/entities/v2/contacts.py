from typing import Annotated

from pydantic import BaseModel
from pydantic import Extra
from pydantic import Field

from ddd.contacts.entities import v1


class Contacts(BaseModel):
    class Config:
        extra = Extra.forbid

    __root__: Annotated[
        list[v1.Contact],
        Field(
            description="list with Contacts",
            title=f"list[{v1.Contact.__name__}]",
        ),
    ]


class ContactData(v1.ContactData):
    pass


class Contact(v1.Contact):
    pass


class ContactPatch(v1.ContactPatch):
    pass


__all__ = (
    "Contact",
    "ContactData",
    "ContactPatch",
    "Contacts",
)
