from uuid import UUID

import pytest
from pydantic.error_wrappers import ValidationError

from ddd.contacts.entities.v1 import Contact
from ddd.contacts.entities.v1 import ContactData
from ddd.contacts.entities.v1 import ContactPatch

pytestmark = [
    pytest.mark.unit,
]


def test_contact_can_be_created() -> None:
    contact_id = UUID("ed8b1c69-2e6d-4c3a-8cdc-584d80dc6e9a")
    contact_name = f"test-name-{contact_id}"
    contact_phone = f"test-phone-{contact_id}"

    contact = Contact(
        id=contact_id,
        name=contact_name,
        phone=contact_phone,
    )

    assert contact.id == contact_id
    assert contact.name == contact_name
    assert contact.phone == contact_phone


def test_contact_no_extra_fields_allowed() -> None:
    exc_info: pytest.ExceptionInfo
    with pytest.raises(ValidationError) as exc_info:
        Contact(
            id=UUID("ed8b1c69-2e6d-4c3a-8cdc-584d80dc6e9a"),
            name="name",
            phone="phone",
            unknown="unknown",  # type:ignore[call-arg]
        )

    exc: ValidationError = exc_info.value
    assert isinstance(exc, ValidationError)
    assert exc.errors()[0]["loc"] == ("unknown",)
    assert exc.errors()[0]["type"] == "value_error.extra"


def test_contact_data_can_be_created() -> None:
    contact_name = "test-name"
    contact_phone = "test-phone"

    contact = ContactData(
        name=contact_name,
        phone=contact_phone,
    )

    assert contact.name == contact_name
    assert contact.phone == contact_phone


def test_contact_data_id_forbidden() -> None:
    exc_info: pytest.ExceptionInfo
    with pytest.raises(ValidationError) as exc_info:
        ContactData(
            id=UUID("ed8b1c69-2e6d-4c3a-8cdc-584d80dc6e9a"),  # type:ignore
            name="name",
            phone="phone",
        )

    exc: ValidationError = exc_info.value
    assert isinstance(exc, ValidationError)
    assert exc.errors()[0]["loc"] == ("id",)
    assert exc.errors()[0]["type"] == "value_error.extra"


def test_contact_patch_can_be_created() -> None:
    contact_name = "test-name"
    contact_phone = "test-phone"

    patch1 = ContactPatch(name=contact_name)
    assert patch1.name == contact_name
    assert patch1.phone is None

    patch2 = ContactPatch(phone=contact_phone)
    assert patch2.name is None
    assert patch2.phone == contact_phone

    patch3 = ContactPatch(name=contact_name, phone=contact_phone)
    assert patch3.name == contact_name
    assert patch3.phone == contact_phone


def test_patch_requires_at_least_one_field() -> None:
    exc_info: pytest.ExceptionInfo
    with pytest.raises(ValidationError) as exc_info:
        ContactPatch()

    exc: ValidationError = exc_info.value
    assert isinstance(exc, ValidationError)
    assert exc.errors()[0]["loc"] == ("__root__",)
    assert exc.errors()[0]["msg"] == "either `name` or `phone` is required"
    assert exc.errors()[0]["type"] == "value_error"


def test_patch_forbids_id() -> None:
    exc_info: pytest.ExceptionInfo
    with pytest.raises(ValidationError) as exc_info:
        ContactPatch(
            id=UUID("ed8b1c69-2e6d-4c3a-8cdc-584d80dc6e9a"),  # type:ignore
            name="name",
            phone="phone",
        )

    exc: ValidationError = exc_info.value
    assert isinstance(exc, ValidationError)
    assert exc.errors()[0]["loc"] == ("id",)
    assert exc.errors()[0]["type"] == "value_error.extra"
