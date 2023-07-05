from typing import Annotated
from uuid import UUID

from pydantic import BaseModel
from pydantic import Extra
from pydantic import Field
from pydantic import root_validator


class ContactFields:
    id = Field(  # noqa: A003,VNE003
        description="Unique identifier of Contact",
        title="ID",
    )

    name = Field(
        description="Full name of Contact, non-empty text",
        min_length=1,
        title="Full name",
    )

    phone = Field(
        description="Phone number of Contact, non-empty text",
        min_length=1,
        title="Phone",
    )


class ContactData(BaseModel):
    class Config:
        extra = Extra.forbid
        orm_mode = True
        title = "Contact Data"

    name: Annotated[str, ContactFields.name]
    phone: Annotated[str, ContactFields.phone]


class Contact(ContactData):
    id: Annotated[UUID, ContactFields.id]  # noqa: A003,VNE003


class ContactPatch(BaseModel):
    class Config:
        extra = Extra.forbid
        orm_mode = True
        title = "Contact Patch"

    name: Annotated[str | None, ContactFields.name] = None
    phone: Annotated[str | None, ContactFields.phone] = None

    @root_validator(pre=True)
    def check_one_field_is_set(cls, values: dict) -> dict:  # noqa: N805
        if (values.get("name") is None) and (values.get("phone") is None):
            raise ValueError("either `name` or `phone` is required")
        return values


class Contacts(BaseModel):
    class Config:
        extra = Extra.forbid

    items: Annotated[
        list[Contact],
        Field(
            description="list with Contacts",
            title=f"list[{Contact.__name__}]",
        ),
    ]


__all__ = (
    "Contact",
    "ContactData",
    "ContactPatch",
    "Contacts",
)
