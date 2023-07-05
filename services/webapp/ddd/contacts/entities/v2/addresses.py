from typing import Annotated
from uuid import UUID

from pydantic import BaseModel
from pydantic import Extra
from pydantic import Field
from pydantic.class_validators import root_validator


class AddressFields:
    id = Field(  # noqa: A003,VNE003
        description="Unique identifier of Address",
        title="ID",
    )

    city = Field(
        description="City name",
        min_length=1,
        title="City",
    )

    contact = Field(
        description="Contact ID",
        title="Contact ID",
    )

    street = Field(
        description="Full name of street",
        min_length=1,
        title="Street",
    )


class AddressData(BaseModel):
    class Config:
        extra = Extra.forbid
        orm_mode = True
        title = "Address Data"

    city: Annotated[str, AddressFields.city]
    contact: Annotated[UUID | None, AddressFields.contact] = None
    street: Annotated[str, AddressFields.street]


class Address(AddressData):
    id: Annotated[int, AddressFields.id]  # noqa: A003,VNE003


class Addresses(BaseModel):
    class Config:
        extra = Extra.forbid
        title = "Addresses"

    __root__: Annotated[
        list[Address],
        Field(
            description="list with Addresses",
            title=f"list[{Address.__name__}]",
        ),
    ]


class AddressPatch(BaseModel):
    class Config:
        extra = Extra.forbid
        orm_mode = True
        title = "Address Patch"

    city: Annotated[str | None, AddressFields.city] = None
    contact: Annotated[UUID | None, AddressFields.contact] = None
    street: Annotated[str | None, AddressFields.street] = None

    @root_validator(pre=True)
    def check_one_field_is_set(cls, values: dict) -> dict:  # noqa: N805
        if all(
            (values.get(f) is None)
            for f in {
                "city",
                "contact",
                "street",
            }
        ):
            raise ValueError("one of [contact, city, street] is required")
        return values


__all__ = (
    "Address",
    "AddressData",
    "Addresses",
    "AddressPatch",
)
